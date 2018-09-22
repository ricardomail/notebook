#### Canvas绘制文字的方式

1. **drawText(String text, float x, float y, Paint paint)**

   文字的基本绘制方式

   ```java
   String text = "Hello HenCoder";
   
   ...
   
   canvas.drawText(text, 200, 100, paint);  
   ```

   这里面文字的x, y坐标指的是文字text的左下角位置

2. **drawTextOnPath(Path path, Paint paint) 沿着一条路径绘制文字**

   ```java
   canvas.drawPath(path, paint); // 把 Path 也绘制出来，理解起来更方便  
   canvas.drawTextOnPath("Hello HeCoder", path, 0, 0, paint);  
   ```

   ```
   drawTextOnPath(String text, Path path, float hOffset, float vOffset, Paint paint)
   ```

   参数里，需要解释的只有两个： `hOffset` 和 `vOffset`。它们是文字相对于 `Path` 的水平偏移量和竖直偏移量，利用它们可以调整文字的位置。例如你设置 `hOffset` 为 5， `vOffset` 为 10，文字就会右移 5 像素和下移 10 像素。

3. **StaticLayout**

   普通的drawText()不能进行换行，所以需要引用StaticLayout来进行操作，但他不能设置位置，只能用Canvas.Translate()来进行位置变换。支持长度和`\n`换行。

   `taticLayout` 的构造方法是 StaticLayout(CharSequence source, TextPaint paint, int width, Layout.Alignment align, float spacingmult, float spacingadd, boolean includepad)，其中参数里：

   `width` 是文字区域的宽度，文字到达这个宽度后就会自动换行； 
   `align` 是文字的对齐方向； 
   `spacingmult` 是行间距的倍数，通常情况下填 1 就好； 
   `spacingadd` 是行间距的额外增加值，通常情况下填 0 就好； 
   `includeadd` 是指是否在文字上下添加额外的空间，来避免某些过高的字符的绘制出现越界。

   ```java
   String text1 = "Lorem Ipsum is simply dummy text of the printing and typesetting industry.";  
   StaticLayout staticLayout1 = new StaticLayout(text1, paint, 600,  
           Layout.Alignment.ALIGN_NORMAL, 1, 0, true);
   String text2 = "a\nbc\ndefghi\njklm\nnopqrst\nuvwx\nyz";  
   StaticLayout staticLayout2 = new StaticLayout(text2, paint, 600,  
           Layout.Alignment.ALIGN_NORMAL, 1, 0, true);
   
   ...
   
   canvas.save();  
   canvas.translate(50, 100);  
   staticLayout1.draw(canvas);  
   canvas.translate(0, 200);  
   staticLayout2.draw(canvas);  
   canvas.restore();  
   ```

4. **setTextSize(float size)**：更改文字大小

5. **setTypeface()**：更改文字字体

6. ```java
   paint.setTypeface(Typeface.createFromAsset(getContext().getAssets(), "Satisfy-Regular.ttf"));  
   canvas.drawText(text, 100, 450, paint);  
   ```

7. **setFakeBlodText(boolean fakeBoldText)**

   是否使用伪粗体

8. **setStrikeThruText(boolean strike)**

   是否增加删除线

9. **setUnderlineText(boolean underlineText)**

   是否增加下划线

   ```java
   paint.setUnderlineText(true);  
   canvas.drawText(text, 100, 150, paint);  
   ```

10. **setTextSkewX(float skew)**

    横向错切

    ```java
    paint.setUnderlineText(true);  
    canvas.drawText(text, 100, 150, paint);  
    ```

11. **setTextScaleX(float scaleX)**

    设置文字横向放缩，也就是文字的变胖变瘦

    ```java
    paint.setTextScaleX(1);  
    canvas.drawText(text, 100, 150, paint);  
    paint.setTextScaleX(0.8f);  
    canvas.drawText(text, 100, 230, paint);  
    paint.setTextScaleX(1.2f);  
    canvas.drawText(text, 100, 310, paint);  
    ```

12. **setletterSpacing(float letterSpacing)**

    设置字符间距，默认值为0

    ```java
    paint.setLetterSpacing(0.2f);  
    canvas.drawText(text, 100, 150, paint);  
    ```

13. **setTextAlign(Paint.Align align)**

    设置文字对其方式  LEFT, RIGHT CENTER

14. **getFontSpacing()**

    获取文字的行间距，两个baseline之间的距离

    ```java
    canvas.drawText(texts[0], 100, 150, paint);  
    canvas.drawText(texts[1], 100, 150 + paint.getFontSpacing, paint);  
    canvas.drawText(texts[2], 100, 150 + paint.getFontSpacing * 2, paint);  
    ```

15. **getTextBounds(String text, int start, int end, Rect bounds)**

    参数里，`text` 是要测量的文字，`start` 和 `end` 分别是文字的起始和结束位置，`bounds` 是存储文字显示范围的对象，方法在测算完成之后会把结果写进 `bounds`。以左上角为基准，测量的数据存储在 bounds中。

16. **float measureText(String text)**

    测量文字宽度并返回，如果你用代码分别使用 `getTextBounds()` 和 `measureText()` 来测量文字的宽度，你会发现 `measureText()` 测出来的宽度总是比 `getTextBounds()` 大一点点。这是因为这两个方法其实测量的是两个不一样的东西。

17. **getTextWidths(String text, float[] widths)**

    测量字符串中每个字符的宽度，并把它放入widths中。

