
#--output_format csv

AUCOUSTIC_MODEL = $(HOME)/Documents/MFA/pretrained_models/acoustic/english_mfa.zip
DICTIONARY_MODEL = $(HOME)/Documents/MFA/pretrained_models/dictionary/english_mfa.dict

CORPUS_DIR = ./
ALIGNED_OUT_DIR = ./aligned_out
VALIDATE_OUT_DIR = ./validate_out

t:
	rm -vf $(ALIGNED_OUT_DIR)/*
	mfa align \
	  $(CORPUS_DIR) $(DICTIONARY_MODEL) $(AUCOUSTIC_MODEL) \
	  $(ALIGNED_OUT_DIR) \
	  --output_format csv \
	  --beam 100 \
	  --include_original_text \
	  --single_speaker        # handy for a single utterance

v:
	mfa validate $(CORPUS_DIR) $(DICTIONARY_MODEL) $(AUCOUSTIC_MODEL) $(VALIDATE_OUT_DIR)

clean:
	rm -vf $(ALIGNED_OUT_DIR) $(VALIDATE_OUT_DIR)
.PHONY: t v clean
