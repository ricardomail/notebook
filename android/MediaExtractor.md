### 一 MediaExtractor

`音视频文件是由音频和视频数据组成的，可以通过MediaExtractor进行抽取`

主要api介绍

* setDataSource(String path) 可以是网络数据和本地数据
* getTrackCount() 得到源文件的通道数
* getTrackFormat(int index) 获取指定的通道格式
* getSampleTime()返回当前的时间戳
* readSampleData(ByteBuffer byteBuf, int offset) 把指定通道中的数据按照偏移量读取到ByteBuffer中
* advance() 读取下一贞
* release() 读取结束后释放资源

```Java
private void extractorVideo() {
        int videoIndex = -1;
        try {
            mediaExtractor = new MediaExtractor();
            mediaExtractor.setDataSource(inputFilePath); //数据源
            int trackCount = mediaExtractor.getTrackCount();
            for (int i = 0; i < trackCount; i++) {
                MediaFormat trackFormat = mediaExtractor.getTrackFormat(i);
                String string = trackFormat.getString(MediaFormat.KEY_MIME);
                if (string.startsWith("video/")) {
                    videoIndex = i;//得到具体轨道
                    break;
                }
            }
            mediaExtractor.selectTrack(videoIndex);
            MediaFormat trackFormat = mediaExtractor.getTrackFormat(videoIndex);
            mediaMuxer = new MediaMuxer(outputVideoFilePath, MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
            int i = mediaMuxer.addTrack(trackFormat);

            ByteBuffer byteBuffer = ByteBuffer.allocate(1024 * 1024);
            MediaCodec.BufferInfo bufferInfo = new MediaCodec.BufferInfo();
            mediaMuxer.start();

            long videoSampleTime;
            //获取每一帧的时间
            {
                mediaExtractor.readSampleData(byteBuffer, 0);
                if (mediaExtractor.getSampleFlags() == MediaExtractor.SAMPLE_FLAG_SYNC) {
                    mediaExtractor.advance();
                }
                mediaExtractor.readSampleData(byteBuffer, 0);
                long sampleTime = mediaExtractor.getSampleTime();
                mediaExtractor.advance();

                mediaExtractor.readSampleData(byteBuffer, 0);
                long sampleTime1 = mediaExtractor.getSampleTime();
                videoSampleTime = Math.abs(sampleTime - sampleTime1);
            }
            //重新选择 否则会丢掉上面的三帧
            mediaExtractor.unselectTrack(videoIndex);
            mediaExtractor.selectTrack(videoIndex);

            while (true) {
                int data = mediaExtractor.readSampleData(byteBuffer, 0);
                if (data < 0) {
                    break;
                }

                bufferInfo.size = data;
                bufferInfo.offset = 0;
                bufferInfo.flags = mediaExtractor.getSampleFlags();
                bufferInfo.presentationTimeUs += videoSampleTime;

                mediaMuxer.writeSampleData(i, byteBuffer, bufferInfo);

                mediaExtractor.advance();
            }
            Toast.makeText(this, "ok", Toast.LENGTH_SHORT).show();

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            mediaExtractor.release();
            mediaMuxer.stop();
            mediaMuxer.release();
        }
    }
```

纯音频:

```java
private void extractorAudio() {
        mediaExtractor = new MediaExtractor();
        int audioIndex = -1;
        try {
            mediaExtractor.setDataSource(inputFilePath);
            int trackCount = mediaExtractor.getTrackCount();
            for (int i = 0; i < trackCount; i++) {
                MediaFormat trackFormat = mediaExtractor.getTrackFormat(i);
                String string = trackFormat.getString(MediaFormat.KEY_MIME);
                if (string.startsWith("audio/")) {
                    audioIndex = i;
                }
            }
            mediaExtractor.selectTrack(audioIndex);
            MediaFormat trackFormat = mediaExtractor.getTrackFormat(audioIndex);
            mediaMuxer = new MediaMuxer(outputAudioFilePath, MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);

            int i = mediaMuxer.addTrack(trackFormat);
            mediaMuxer.start();

            ByteBuffer byteBuffer = ByteBuffer.allocate(1024 * 1024);
            MediaCodec.BufferInfo bufferInfo = new MediaCodec.BufferInfo();

            long time;
            {
                mediaExtractor.readSampleData(byteBuffer, 0);
                if (mediaExtractor.getSampleFlags() == MediaExtractor.SAMPLE_FLAG_SYNC) {
                    mediaExtractor.advance();
                }
                mediaExtractor.readSampleData(byteBuffer, 0);
                long sampleTime = mediaExtractor.getSampleTime();
                mediaExtractor.advance();

                mediaExtractor.readSampleData(byteBuffer, 0);
                long sampleTime1 = mediaExtractor.getSampleTime();
                mediaExtractor.advance();

                time = Math.abs(sampleTime - sampleTime1);
            }

            mediaExtractor.unselectTrack(audioIndex);
            mediaExtractor.selectTrack(audioIndex);
            while (true) {
                int data = mediaExtractor.readSampleData(byteBuffer, 0);
                if (data < 0) {
                    break;
                }

                bufferInfo.size = data;
                bufferInfo.flags = mediaExtractor.getSampleFlags();
                bufferInfo.offset = 0;
                bufferInfo.presentationTimeUs += time;

                mediaMuxer.writeSampleData(i, byteBuffer, bufferInfo);
                mediaExtractor.advance();
            }


            Toast.makeText(this, "ok", Toast.LENGTH_SHORT).show();

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            mediaExtractor.release();
            mediaMuxer.stop();
            mediaMuxer.release();
        }
    }
```

### 二 aac的ADTS头

当编码AAC裸流的时候，aac文件并不能在pc和手机上播放，很大的可能就是aac文件中每一帧里都缺少了ADTS头信息，AAC音频文件的每一帧由ADTS Header和AAC Audio Data组成

![img](https://img-blog.csdn.net/20161028125743877?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

![img](https://img-blog.csdn.net/20161028130235945?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

* syncword ：总是0xFFF, 代表一个ADTS帧的开始, 用于同步.
* 解码器可通过0xFFF确定每个ADTS的开始位置.
* 因为它的存在，解码可以在这个流中任何位置开始, 即可以在任意帧解码。
* ID：MPEG Version: 0 for MPEG-4，1 for MPEG-2
* Layer：always: '00'
* protection_absent：Warning, set to 1 if there is no CRC and 0 if there is CRC
* profile：表示使用哪个级别的AAC，如01 Low Complexity(LC) -- AAC LC
* profile的值等于 Audio Object Type的值减1.
* Profile = MPEG-4 Audio Object Type -1

```java
    /**

- 添加ADTS头
- @param packet
- @param packetLen
/
    private void addADTStoPacket(byte[] packet, int packetLen) {
			int profile = 2; // AAC LC
			int freqIdx = 4; // 44.1KHz
			int chanCfg = 2; // CPE

    // fill in ADTS data
      packet[0] = (byte) 0xFF;
      packet[1] = (byte) 0xF9;
      packet[2] = (byte) (((profile - 1) << 6) + (freqIdx << 2) + (chanCfg >> 2));
      packet[3] = (byte) (((chanCfg & 3) << 6) + (packetLen >> 11));
      packet[4] = (byte) ((packetLen & 0x7FF) >> 3);
      packet[5] = (byte) (((packetLen & 7) << 5) + 0x1F);
      packet[6] = (byte) 0xFC;
    }
```

---------------------
