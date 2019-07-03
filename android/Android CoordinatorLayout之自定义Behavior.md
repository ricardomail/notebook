#### CoordinatorLayout

design库里的核心空间，实现view之间嵌套滑动等交互操作

##### Behavior

一般来说Coordinatorlayout会作为布局的根view，并会给相应的子View添加一个属性`app:layout_behavior=`,自定义behavior需要事先在@String文件中声明一下，然后就可以调用了

```java
public static abstract class Behavior<V extends View> {

        public Behavior() {
        }

        public Behavior(Context context, AttributeSet attrs) {
        }
       //省略了若干方法
}

```

指定behavior的View类型，可以有以下几种方式重写：

`onInterceptTouchEvent()`：是否拦截触摸事件

 `onTouchEvent()`：处理触摸事件

 `layoutDependsOn()`：确定使用`Behavior`的`View`要依赖的`View`的类型

 `onDependentViewChanged()`：当被依赖的`View`状态改变时回调

 `onDependentViewRemoved()`：当被依赖的`View`移除时回调

 `onMeasureChild()`：测量使用`Behavior`的`View`尺寸

 `onLayoutChild()`：确定使用`Behavior`的`View`位置

 `onStartNestedScroll()`：嵌套滑动开始（`ACTION_DOWN`），确定`Behavior`是否要监听此次事件

 `onStopNestedScroll()`：嵌套滑动结束（`ACTION_UP`或`ACTION_CANCEL`）

 `onNestedScroll()`：嵌套滑动进行中，要监听的子 `View`的滑动事件已经被消费

 `onNestedPreScroll()`：嵌套滑动进行中，要监听的子 `View`将要滑动，滑动事件即将被消费（但最终被谁消费，可以通过代码控制）

 `onNestedFling()`：要监听的子 `View`在快速滑动中

 `onNestedPreFling()`：要监听的子`View`即将快速滑动



1. layoutDependsOn:确定提供的子视图是否具有另一个特定的兄弟视图作为布局依赖关系，即用来确定依赖关系，如果某个控件需要依赖控件，就重写该方法

   ```java
   @Override
       public boolean layoutDependsOn(CoordinatorLayout parent， View child， View dependency) {
           return dependency instanceof AppBarLayout;
       }
   
   ```

2. onDependentViewChanged:依赖视图的大小，位置发生变化时调用该方法，重写此方法可以处理child的响应

3. onStartNestedScroll：当CoordinatorLayout的子view开始嵌套滑动时（此处的滑动View必须实现NestedScrollingChild接口），触发此方法，添加Behavior的控件需要为CoordinatorLayout的直接子View，否则不会继续流程

   ```java
   //判断是否垂直滑动
       @Override
       public boolean onStartNestedScroll(CoordinatorLayout coordinatorLayout， View child， View directTargetChild， View target， int nestedScrollAxes) {
           return (nestedScrollAxes & ViewCompat.SCROLL_AXIS_VERTICAL) != 0;
       }
   
   ```

4. onNestedPreScroll:此方法中consumed指的是父布局要消耗的滚动距离，consumed[0]为水平方向消耗的距离，[1]为垂直方向消耗的距离，可控制此参数作出响应调整，如垂直滑动时，若设置consumed[1]=dy，则代表父布局全部消耗了滑动距离，类似AppBarLayout这种效果

   ```java
   /**
        * 触发滑动嵌套滚动之前调用的方法
        *
        * @param coordinatorLayout coordinatorLayout父布局
        * @param child             使用Behavior的子View
        * @param target            触发滑动嵌套的View(实现NestedScrollingChild接口)
        * @param dx                滑动的X轴距离
        * @param dy                滑动的Y轴距离
        * @param consumed          父布局消费的滑动距离，consumed[0]和consumed[1]代表X和Y方向父布局消费的距离，默认为0
        */
       @Override
       public void onNestedPreScroll(CoordinatorLayout coordinatorLayout， View child， View target， 
           int dx， int dy， int[] consumed) {
           super.onNestedPreScroll(coordinatorLayout， child， target， dx， dy， consumed);
       }
   
   ```

5. onNestedScroll:此方法中dyConsumed代表TargetView消费的距离，如RecyclerView滑动的距离，可通过控制NestScrollingChild的滑动来指定一些动画，
    本篇博客实现的效果主要就是重写此方法，若根据onNestedPreScroll中dy来判断，则当RecyclerView条目很少时，也会触发逻辑代码，故选择了重写此方法。

   ```java
   /**
        * 滑动嵌套滚动时触发的方法
        *
        * @param coordinatorLayout coordinatorLayout父布局
        * @param child             使用Behavior的子View
        * @param target            触发滑动嵌套的View
        * @param dxConsumed        TargetView消费的X轴距离
        * @param dyConsumed        TargetView消费的Y轴距离
        * @param dxUnconsumed      未被TargetView消费的X轴距离
        * @param dyUnconsumed      未被TargetView消费的Y轴距离(如RecyclerView已经到达顶部或底部，
        *              而用户继续滑动，此时dyUnconsumed的值不为0，可处理一些越界事件)
        */
       @Override
       public void onNestedScroll(CoordinatorLayout coordinatorLayout， View child， View target， 
           int dxConsumed， int dyConsumed， int dxUnconsumed， int dyUnconsumed) {
           super.onNestedScroll(coordinatorLayout， child， target， 
               dxConsumed， dyConsumed， dxUnconsumed， dyUnconsumed);
       }
   		
   ```



##### 自定义Behavior

实现方式：

1. layoutDependsOn和onDependentViewChanged, child需要依赖于dependency,当dependency View发生变化时，onDependentViewChanged会被调用，child可作出响应
2. 第二种为onStartNestedScroll等嵌套滑动的流程，首先在onStartNestedScroll方法中判断是否垂直滑动等，然后在onNestedPreScroll、onNestedScroll等方法实现效果



第二种具体实现：

1. 嵌套滑动开始之前，可以判断是否为垂直滑动，做一些初始化工作，比如获取childView的初始坐标

   ```java
   //判断垂直滑动
       @Override
       public boolean onStartNestedScroll(CoordinatorLayout coordinatorLayout, View child, View directTargetChild, View target, int nestedScrollAxes) {
           if (isInit) {// 设置标记，防止new Anim导致的parent和child坐标变化
               mCommonAnim = new LTitleBehaviorAnim(child);
               isInit = false;
           }
           return (nestedScrollAxes & ViewCompat.SCROLL_AXIS_VERTICAL) != 0;
       }
   	
   ```

2. 触发嵌套滑动之前，可以在此处判断一些滑动手势，以及父布局的消费情况。由于若根据此方法中dy来判断，则当RecyclerView条目很少时，也会触发逻辑代码，故本文只是在此方法中给动画做一些自定义操作。

   ```java
   @Override
       public void onNestedPreScroll(CoordinatorLayout coordinatorLayout, View child, View target, int dx, int dy, int[] consumed) {
           if (mCommonAnim != null) {
               mCommonAnim.setDuration(mDuration);
               mCommonAnim.setInterpolator(mInterpolator);
           }
           super.onNestedPreScroll(coordinatorLayout, child, target, dx, dy, consumed);
       }
   
   ```

3. 滑动嵌套滚动时触发的方法，以Title(Toolbar)为例，若向上滑动，则隐藏Toolbar，反之显示。

   ```java
   @Override
       public void onNestedScroll(CoordinatorLayout coordinatorLayout, View child, View target, int dxConsumed, int dyConsumed, int dxUnconsumed, int dyUnconsumed) {
           super.onNestedScroll(coordinatorLayout, child, target, dxConsumed, dyConsumed, dxUnconsumed, dyUnconsumed);
           if (dyConsumed < 0) {
               if (isHide) {
                   mCommonAnim.show();
                   isHide = false;
               }
           } else if (dyConsumed > 0) {
               if (!isHide) {
                   mCommonAnim.hide();
                   isHide = true;
               }
           }
       }
   
   ```

https://www.jianshu.com/p/2974d8ffc3a5

https://www.jianshu.com/p/b987fad8fcb4