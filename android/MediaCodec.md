### 一 MediaCodec

`MediaCodec类可以用于使用一些基本的多媒体编解码器（音视频编解码组件）`

编码器可以处理输入的数据产生输出的数据，编解码器使用一组输入和输出缓冲器来异步处理数据

![img](https://images2017.cnblogs.com/blog/682616/201709/682616-20170912183105016-1579199179.png)

#### 支持的数据类型

**编解码器能处理的数据类型为：****压缩数据、原始音频数据和原始视频数据。**你可以通过ByteBuffers能够处理这三种数据，但是需要你提供一个Surface，用于对原始的视频数据进行展示，这样也能提高编解码的性能。Surface使用的是本地的视频缓冲区，这个缓冲区不映射或拷贝到ByteBuffers。这样的机制让编解码器的效率更高。通常在使用Surface的时候，无法访问原始的视频数据，但是你可以使用ImageReader访问解码后的原始视频帧。在使用ByteBuffer的模式下，您可以使用Image类和getInput/OutputImage（int）访问原始视频帧。 

![img](https://images2017.cnblogs.com/blog/682616/201709/682616-20170913105110891-222810539.png)

1. 当创建编解码器的时候处于未初始化状态。首先你需要调用configure(…)方法让它处于Configured状态，然后调用start()方法让其处于Executing状态。在Executing状态下，你就可以使用上面提到的缓冲区来处理数据。
2. Executing的状态下也分为三种子状态：Flushed, Running、End-of-Stream。在start() 调用后，编解码器处于Flushed状态，这个状态下它保存着所有的缓冲区。一旦第一个输入buffer出现了，编解码器就会自动运行到Running的状态。当带有end-of-stream标志的buffer进去后，编解码器会进入End-of-Stream状态，这种状态下编解码器不在接受输入buffer，但是仍然在产生输出的buffer。此时你可以调用flush()方法，将编解码器重置于Flushed状态。
3. 调用stop()将编解码器返回到未初始化状态，然后可以重新配置。 完成使用编解码器后，您必须通过调用release()来释放它。
4. 在极少数情况下，编解码器可能会遇到错误并转到错误状态。 这是使用来自排队操作的无效返回值或有时通过异常来传达的。 调用reset()使编解码器再次可用。 您可以从任何状态调用它来将编解码器移回未初始化状态。 否则，调用 release()动到终端释放状态。

MediaCodec可以处理具体的视频流，主要有这几个方法：

- getInputBuffers：获取需要编码数据的输入流队列，返回的是一个ByteBuffer数组 
- queueInputBuffer：输入流入队列 
- dequeueInputBuffer：从输入流队列中取数据进行编码操作 
- getOutputBuffers：获取编解码之后的数据输出流队列，返回的是一个ByteBuffer数组 
- dequeueOutputBuffer：从输出队列中取出编码操作之后的数据 
- releaseOutputBuffer：处理完成，释放ByteBuffer数据 

### Android 硬编码流控

MediaCodec 流控相关的接口并不多，一是配置时设置目标码率和码率控制模式，二是动态调整目标码率(Android 19 版本以上)。

配置时指定目标码率和码率控制模式：

```
mediaFormat.setInteger(MediaFormat.KEY_BIT_RATE, bitRate);
mediaFormat.setInteger(MediaFormat.KEY_BITRATE_MODE,
MediaCodecInfo.EncoderCapabilities.BITRATE_MODE_VBR);
mVideoCodec.configure(mediaFormat, null, null, MediaCodec.CONFIGURE_FLAG_ENCODE);
```

码率控制模式有三种：

- CQ  表示完全不控制码率，尽最大可能保证图像质量；
- CBR 表示编码器会尽量把输出码率控制为设定值，即我们前面提到的“不为所动”；
- VBR 表示编码器会根据图像内容的复杂度（实际上是帧间变化量的大小）来动态调整输出码率，图像复杂则码率高，图像简单则码率低；

动态调整目标码率： 

```
Bundle param = new Bundle();
param.putInt(MediaCodec.PARAMETER_KEY_VIDEO_BITRATE, bitrate);
mediaCodec.setParameters(param);
```

### 3.3 Android 流控策略选择

- 质量要求高、不在乎带宽、解码器支持码率剧烈波动的情况下，可以选择 CQ 码率控制策略。
- VBR 输出码率会在一定范围内波动，对于小幅晃动，方块效应会有所改善，但对剧烈晃动仍无能为力；连续调低码率则会导致码率急剧下降，如果无法接受这个问题，那 VBR 就不是好的选择。
- CBR 的优点是稳定可控，这样对实时性的保证有帮助。所以 WebRTC 开发中一般使用的是CBR。