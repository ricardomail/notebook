### 作用

测量View的宽/高

1. 某些情况下，需要多次测量才能确定view的最终的宽高
2. 该情况下，measure过程后得到的宽/高可能不准确
3. 可以考虑在onLayout()方法中去获取最终的宽高

### ViewGroup.LayoutParams类

布局参数类，指定视图View的高度和宽度等布局参数

![img](https://mmbiz.qpic.cn/mmbiz_png/vEMApYVjEzfEVK8WdILm9ibrr3zD8b5pbO1oDg8JNMkQxepFlr7zfdWvtgKUHcrFv8mnmGudERHw5AiccK8RzKicg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

### 单一view的绘制流程

![img](https://mmbiz.qpic.cn/mmbiz_png/vEMApYVjEzfEVK8WdILm9ibrr3zD8b5pbxWbtWPSZPJ0W5c6c7sZBaXv8n7DDpafnhBM8Uac15nLypqFPzXZwpQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

Measure过程的入口是：measure()

measure()方法不可被重写，方法中调用onMeasure()方法，可以通过重写onMeasure()方法来实现计算

onMeasure()中调用

```java
 setMeasuredDimension(getDefaultSize(getSuggestedMinimumWidth(), widthMeasureSpec),  
                         getDefaultSize(getSuggestedMinimumHeight(), heightMeasureSpec));  
```

用来存储测量的宽高

getDefaultSize(int size, int measureSpec)方法用来测量规格，计算View的宽/高值

```java
 public static int getDefaultSize(int size, int measureSpec) {  

        // 参数说明：
        // size：提供的默认大小
        // measureSpec：宽/高的测量规格（含模式 & 测量大小）

            // 设置默认大小
            int result = size; 

            // 获取宽/高测量规格的模式 & 测量大小
            int specMode = MeasureSpec.getMode(measureSpec);  
            int specSize = MeasureSpec.getSize(measureSpec);  

            switch (specMode) {  
                // 模式为UNSPECIFIED时，使用提供的默认大小 = 参数Size
                case MeasureSpec.UNSPECIFIED:  
                    result = size;  
                    break;  

                // 模式为AT_MOST,EXACTLY时，使用View测量后的宽/高值 = measureSpec中的Size
                case MeasureSpec.AT_MOST:  
                case MeasureSpec.EXACTLY:  
                    result = specSize;  
                    break;  
            }  

         // 返回View的宽/高值
            return result;  
        }    
```



默认大小和背景有关

```java
protected int getSuggestedMinimumWidth() {
    return (mBackground == null) ? mMinWidth : max(mMinWidth,mBackground.getMinimumWidth());
}
```

如果没有默认背景，View的宽度就等于mMinWidth，也就等于android:minWidth属性，没指定的时候默认为0

如果设置了背景，取mMinWidth和背景的最大值



![img](https://mmbiz.qpic.cn/mmbiz_png/vEMApYVjEzfEVK8WdILm9ibrr3zD8b5pbY3TpWp2q2eOYSUIcxiaj5ZiaCTlsvT2WIIRechKmLSXj9YoQv7lc2tWQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)



