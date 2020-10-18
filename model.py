from spectralcluster import SpectralClusterer
from resemblyzer import VoiceEncoder
from resemblyzer.hparams import sampling_rate


def clustering(wav):
    encoder = VoiceEncoder("cpu")
    _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16) #create d-vectors
    clusterer = SpectralClusterer(
            min_clusters=2,
            max_clusters=100,
            p_percentile=0.90,
            gaussian_blur_sigma=1)

    labels = clusterer.predict(cont_embeds)
    times = [((s.start + s.stop) / 2) / sampling_rate for s in wav_splits]
    labelling = []
    start_time = 0

    for i, time in enumerate(times):
        if i > 0 and labels[i] != labels[i-1]:
            temp = ['speaker '+str(labels[i-1]), start_time, time]
            labelling.append(tuple(temp))
            start_time = time
        if i == len(times)-1:
            temp = ['speaker '+str(labels[i]), start_time, time]
            labelling.append(tuple(temp))
    return labelling #str
