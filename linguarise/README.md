
# English Learning Project

A comprehensive language learning project focused on improving English proficiency through various methods, particularly shadow learning.

## Overview
- Primary focus on English language acquisition
- Uses shadow learning as the main learning technique
- Plans to expand to other language learning aspects
- Future scope includes application to other languages

## What is Shadow Learning?
Shadow learning is a language learning technique where learners closely mimic or "shadow" native speakers, repeating what they hear in real-time. This method helps improve:
- Pronunciation
- Intonation
- Speaking rhythm
- Listening comprehension

## Future Development
- Integration of additional learning methodologies
- Expansion to cover more language aspects (grammar, vocabulary, writing)
- Support for multiple languages
- Enhanced learning tools and resources

## Install MFA(Montreal Forced Aligner)

```bash
 conda deactivate
 conda remove --name  aligner --all
 conda create -n aligner -c conda-forge  python=3.10
 conda activate aligner
 conda install  kaldi pynini
 pip install montreal-forced-aligner
 python -c "from _kalpy.gmm import AccumAmDiagGmm; print('Kalpy bindings loaded successfully')"\n
 mfa
 pip install --upgrade "joblib>=1.3"\n
 conda install -c conda-forge joblib=1.3.2\n
 mfa
 mfa --help
```

```bash
 mfa models download acoustic english_mfa
 mfa models download dictionary english_mfa
```




## Reference
- [MFA Montreal Force Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/index.html#first-steps)













