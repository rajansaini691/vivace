* Use essentia library for processing and event detection (replace FFT) instead
  of numpy
  * https://essentia.upf.edu/documentation/FAQ.html#using-essentia-real-time
    * Information on real-time usage of essentia
  * We want streaming data
  * Low-hanging fruit: pitch estimator for monophonic music, RhythmExtractor
