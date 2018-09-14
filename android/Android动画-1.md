## ViewPropertyAnimator  09142018

#### 使用方式： View.animate()后面跟一些动画方法即可

1. **translationX**：延x轴移动
2. **translationY**:   延Y轴移动
3. **translationZ**:   延Z轴移动 （版本大于等于Build.VERSION_CODES.LOLLIPOP）时可用
4. **rotation**: 平面旋转
5. **rotationX**: 延x轴立体旋转
6. **rotationY**：延Y轴立体旋转
7. **scaleX**: 延x轴缩放
8. **scaleY**: 延y轴缩放
9. **alpha**: 动画改变透明度
10. **setDuration(ms)**: 设置动画时常，内容为毫秒

#### 动画组合

```java
imageView.animate().translationX(Utils.dpToPixel(200))
        .alpha(1)
        .scaleX(1)
        .scaleY(1)
        .rotation(720);
```

#### Interpolator 速度设置器

setInterpolator(). 设置速度设置器

1. **AccelerateDecelerateInterpolator**： 现加速后减速，为默认加速器
2. **LinearInterpolator**： 匀速
3. **AccelerateInterpolator**： 持续加速
4. **DecelerateInterpolator**：持续减速
5. **AnticipateInterpolator**：先会拉在进行正常轨迹绘制，有点像蓄力
6. **OvershootInterpolator**：动画会超过目标值一些，然后再弹回来效果有点像坐在沙发上然后弹起来一点点。
7. **AnticipateOvershootInterpolator**： 上面两种的结合版
8. **BounceInterpolator**：目标处弹跳，有点像玻璃球掉在地板上
9. **CycleInterpolator**： 可自定义曲线周期，动画可以不到终点结束，可以到达终点后回弹，回弹次数由参数决定。参数为0.5f 到达终点后返回。
10. **PathInterpolator**： 自定义动画完成度/时间完成度曲线https://hencoder.com/ui-1-6/

#### 动画监听器

1. **ViewPropertyAnimator**
   1. setListener()：`onAnimationStart(Animator animalion)`动画开始执行时，这个方法被调用。`onAnimationEnd(Animator animation)`动画结束时被调用。`onAnimationCancel(Animator animation)`动画被取消是，这个方法调用，end也会被调用。`onAnimationRepeat(Animator animation)`当动画通过`setRepeatMode()`/`setRepeatCount()`或`repeat()`方法重复执行时被调用，但ViewPropertyAnimator不支持重复，所以这个方法对它没用。
   2. setUpdateListener(): `onAnimationUpdate`当动画属性更新时调用。
   3. WithStartAction/EndAction(): ViewPropertyAnimator独有，一次性的，只有在动画正常结束时才能调用end
2. **ObjectAnimator**
   1. addListener(): 同上
   2. addUpdateListener(): 同上
   3. addPauseListener()