#### 1. 作用：

1.1 向RecycleView中的ItemView添加装饰

1.2 具体使用：

``` java
public class TestDividerItemDecoration extends RecyclerView.ItemDecoration {

    // 方法1：getItemOffsets（）
    // 作用：设置ItemView的内嵌偏移长度（inset）
    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
       ...
  }

    // 方法2：onDraw（）
    // 作用：在子视图上设置绘制范围，并绘制内容
    // 类似平时自定义View时写onDraw()一样
    // 绘制图层在ItemView以下，所以如果绘制区域与ItemView区域相重叠，会被遮挡
    @Override
    public void onDraw(Canvas c, RecyclerView parent, RecyclerView.State state) {
    ...
  }

    // 方法3：onDrawOver（）
    // 作用：同样是绘制内容，但与onDraw（）的区别是：绘制在图层的最上层
    @Override
    public void onDrawOver(Canvas c, RecyclerView parent, RecyclerView.State state) {
      ...
}

```

1.3 方法使用

`getItemOffsets()`设置itemView的内嵌偏移长度`insert`

其实RecycleView中的ItemView外面会包裹一个矩形（outRect）内嵌偏移长度是指该矩形outRect与ItemView的间隔 itemview指的是内容视图

![img](https://upload-images.jianshu.io/upload_images/944365-16358b268f1f1515.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

内嵌偏移长度分为四个方向：上、下、左、右，并由outRect中的top、left、right、bottom、参数控制，默认为0

```java
@Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
      // 参数说明：
        // 1. outRect：全为 0 的 Rect（包括着Item）
        // 2. view：RecyclerView 中的 视图Item
        // 3. parent：RecyclerView 本身
        // 4. state：状态

      outRect.set(50, 0, 0,50);
      // 4个参数分别对应左（Left）、上（Top）、右（Right）、下（Bottom）
      // 上述语句代表：左&下偏移长度=50px，右 & 上 偏移长度 = 0
       ...
  }

```



`onDraw()` ： Item decoration的onDraw()绘制会优先于ItemView的onDraw（），所以如**果在Itemdecoration的onDraw()中绘制的内容在ItemView边界内，就会被ItemView遮挡住**

![img](https://upload-images.jianshu.io/upload_images/944365-9a3bada010f87fbc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

```java
@Override
    public void onDraw(Canvas c, RecyclerView parent, 
                                  RecyclerView.State state) {

    // RecyclerView 的左边界加上 paddingLeft距离 后的坐标位置
    final int left = parent.getPaddingLeft();
    // RecyclerView 的右边界减去 paddingRight 后的坐标位置
    final int right = parent.getWidth() - parent.getPaddingRight();
    // 即左右边界就是 RecyclerView 的 ItemView区域

    // 获取RecyclerView的Child view的个数
    final int childCount = parent.getChildCount();

    // 设置布局参数
    final RecyclerView.LayoutParams params = (RecyclerView.LayoutParams) child
                .getLayoutParams();

    // 遍历每个RecyclerView的Child view
    // 分别获取它们的位置信息，然后再绘制内容
    for (int i = 0; i < childCount; i++) {
        final View child = parent.getChildAt(i);
        int index = parent.getChildAdapterPosition(view);
            // 第一个Item不需要绘制
            if ( index == 0 ) {
                continue;
            }
        // ItemView的下边界：ItemView 的 bottom坐标 + 距离RecyclerView底部距离 +translationY
        final int top = child.getBottom() + params.bottomMargin +
                Math.round(ViewCompat.getTranslationY(child));
        // 绘制分割线的下边界 = ItemView的下边界+分割线的高度
        final int bottom = top + mDivider.getIntrinsicHeight();
        mDivider.setBounds(left, top, right, bottom);
        mDivider.draw(c);
    }
}

}

```

绘制分割线可以用得到

`onDrawOver()`作用：和onDraw()类似，onDrawOver绘制是后于ItemView的onDraw（）绘制，不需要考虑遮挡问题

```java
Itemdecoration.onDraw（）`> `ItemView.onDraw()` > `Itemdecoration.onDrawOver（）
```

```java
public class DividerItemDecoration extends RecyclerView.ItemDecoration {
    private Paint mPaint;
    private Bitmap mIcon;

    // 在构造函数里进行绘制的初始化，如画笔属性设置等
    public DividerItemDecoration(Context context) {

        mPaint = new Paint();
        mPaint.setColor(Color.RED);
        // 画笔颜色设置为红色

        // 获取图片资源
        mIcon = BitmapFactory.decodeResource(context.getResources(), R.mipmap.logo);
    }

    // 重写onDrawOver（）
    // 将角度绘制到ItemView上
    @Override
    public void onDrawOver(Canvas c, RecyclerView parent, RecyclerView.State state) {
        super.onDrawOver(c, parent, state);

        // 获取Item的总数
        int childCount = parent.getChildCount();
        // 遍历Item
        for ( int i = 0; i < childCount; i++ ) {
            // 获取每个Item的位置
            View view = parent.getChildAt(i);
            int index = parent.getChildAdapterPosition(view);

            // 设置绘制内容的坐标(ItemView的左边界,ItemView的上边界)
            // ItemView的左边界 = RecyclerView 的左边界 = paddingLeft距离 后的位置
            final int left = parent.getWidth()/2;
            // ItemView的上边界
            float top = view.getTop();

            // 第1个ItemView不绘制
            if ( index == 0 ) {
                continue;
            }
                // 通过Canvas绘制角标
                c.drawBitmap(mIcon,left,top,mPaint);
        }
    }

}

```

时间轴案例：https://www.jianshu.com/p/655ea359e3db

转载自：https://www.jianshu.com/p/9a796bb23a47