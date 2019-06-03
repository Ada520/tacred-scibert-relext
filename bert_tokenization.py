import os
import tokenization
import numpy as np
import json

kDataFile = "../data/tacred/data/json/test.json"
kVocabFile = "../bert/cased_L-12_H-768_A-12/vocab.txt"
kSaveFile = "test_conversion.json"


def transform( datafile, vocabfile ):

    with open( datafile ) as datafile:
        data = json.load( datafile )

    tokenizer = tokenization.FullTokenizer( vocab_file=vocabfile, do_lower_case=False )

    mapping = { '-LRB-': '(',
                '-RRB-': ')',
                '-LSB-': '[',
                '-RSB-': ']',
                '-LCB-': '{',
                '-RCB-': '}',
                    0: '[UNK]',
                    1: '[PAD]' }

    for d in data:
        tokens = d['token']
        s1 = d['subj_start']
        e1 = d['subj_end']
        s2 = d['obj_start']
        e2 = d['obj_end']

        bert_tokens = []
        orig_to_tok_map = []
        tok_len_map = []
        bert_tokens.append( "[CLS]" )
        for token in tokens:
            if token in mapping:
                token = mapping[token]

            orig_to_tok_map.append( len(bert_tokens) )
            bert_tokens.extend( tokenizer.tokenize(token) )
            tok_len_map.append( len(bert_tokens)-orig_to_tok_map[-1] )
        bert_tokens.append( "[SEP]" )

        d['token'] = bert_tokens
        d['subj_start'] = orig_to_tok_map[s1]
        d['subj_end'] = orig_to_tok_map[e1]+1
        d['obj_start'] = orig_to_tok_map[s2]
        d['obj_end'] = orig_to_tok_map[e2]+1

        spos = d['stanford_pos']
        spos2 = ['[CLS]']
        sner = d['stanford_ner']
        sner2 = ['[CLS]']
        shead = d['stanford_head']
        shead2 = ['[CLS]']
        sdep = d['stanford_deprel']
        sdep2 = ['[CLS]']
        for i in range( len(tok_len_map) ):
            n = tok_len_map[i]
            spos2 += [spos[i]]*n
            sner2 += [sner[i]]*n
            shead2 += [shead[i]]*n
            sdep2 += [sdep[i]]*n
        spos2.append( "[SEP]" )
        sner2.append( "[SEP]" )
        shead2.append( "[SEP]" )
        sdep2.append( "[SEP]" )
        d['stanford_pos'] = spos2
        d['stanford_ner'] = sner2
        d['stanford_head'] = shead2
        d['stanford_deprel'] = sdep2

    with open( kSaveFile, 'w' ) as outfile:
        json.dump( data, outfile, indent=2 )



def load_tokens( filename ):
    with open( filename ) as infile:
        data = json.load( infile )
        tokens = []
        for d in data:
            tokens += d['token']
    print( "{} tokens from {} examples loaded from {}.".format( len(tokens), len(data), filename ) )
    return tokens


if __name__ == "__main__":
    transform( kDataFile, kVocabFile )