import enum


class SupportedVideoResolution(enum.Enum):
    RES_144p = '144p'
    RES_240p = '240p'
    RES_360p = '360p'
    RES_480p = '480p'
    RES_720p = '720p'
    RES_1080p = '1080p'
    RES_1440p = '1440p'
    RES_2160p = '2160p'
    RES_4320p = '4320p'


class SupportedVideoFPS(enum.Enum):
    FPS24 = '24fps'
    FPS25 = '25fps'
    FPS30 = '30fps'
    FPS48 = '48fps'
    FPS50 = '50fps'
    FPS60 = '60fps'


class SupportedAudioSampleRate(enum.Enum):
    SAMP_R_44 = '44.1kbps'
    SAMP_R_48 = '48kbps'
    SAMP_R_50 = '50kbps'
    SAMP_R_70 = '70kbps'
    SAMP_R_128 = '128kbps'
    SAMP_R_160 = '160kbps'
    SAMP_R_192 = '192kbps'
    SAMP_R_320 = '320kbps'
