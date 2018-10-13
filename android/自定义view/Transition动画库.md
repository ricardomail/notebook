### Transition framework ----android 动画框架

1. 正常情况下，Android中存在view动画，tween动画以及属性动画，但在Android 4.4时，引入了Transition库，在5.0才得到真正的实现。
2. Transition framework核心是根据场景Scene的不同，来帮助开发者自动生成动画



### Detail

1. 通过以下几种方式开启动画：

   * TransitionManager.go()
   * beginDelayedTransition()
   * setEnterTransition()/ setSharedElementEnterTransition()

2. **TransitionManager.go()**

   Scene类是关键，这个类存储着一个根view下的各种view的属性。通常由`getSceneForLayout(ViewGroup sceneRoot, int layoutId, Context context)`获取实例

   sceneRoot: scene发生改变和动画执行的位置, 发生动画的容器

   layoutId: 根view 场景xml

   ```java
   //开始场景
   mSceneStart = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_bounds_start, mContext);
   //结束场景
   mSceneEnd = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_bounds_end, mContext);
   TransitionManager.go(mSceneStart);
   ```

   动画类库：

   * ChangeBounds
      检测view的位置边界创建移动和缩放动画

     ```java
     mSceneStart = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_bounds_start, mContext);
     mSceneEnd = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_bounds_end, mContext);
     TransitionManager.go(mStartSceneState ? mSceneEnd : mSceneStart, new ChangeBounds());
     ```

   * ChangeTransform
      检测view的scale和rotation创建缩放和旋转动画

     ```java
     mSceneStart = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_transform_start, mContext);
     mSceneEnd = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_transform_end, mContext);
     TransitionManager.go(mStartSceneState ? mSceneEnd : mSceneStart, new ChangeTransform());
     ```


   * ChangeClipBounds
      检测view的剪切区域的位置边界，和ChangeBounds类似。不过ChangeBounds针对的是view而ChangeClipBounds针对的是view的剪切区域(`setClipBound(Rect rect)` 中的rect)。如果没有设置则没有动画效果

     ```java
     View startView = LayoutInflater.from(mContext).inflate(R.layout.scene_change_clip_bounds_start, mSceneRootView, false);
     startView.findViewById(R.id.image_change_clip_bounds).setClipBounds(new Rect(0, 0, 300, 300));
     View endView = LayoutInflater.from(mContext).inflate(R.layout.scene_change_clip_bounds_end, mSceneRootView, false);
     int w = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED);
     int h = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED);
     endView.measure(w, h);
     int height = endView.getMeasuredHeight();
     int width = endView.getMeasuredWidth();
     
     endView.findViewById(R.id.image_change_clip_bounds).setClipBounds(new Rect(0, 0, width, height));
     mSceneStart = new Scene(mSceneRootView, startView);
     mSceneEnd = new Scene(mSceneRootView, endView);
     
     TransitionManager.go(mStartSceneState ? mSceneEnd : mSceneStart, new ChangeClipBounds());
     ```

   * ChangeImageTransform
      检测**ImageView**（这里是专指ImageView）的尺寸，位置以及ScaleType，并创建相应动画。

     ```java
     mSceneStart = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_image_transform_start, mContext);
     mSceneEnd = Scene.getSceneForLayout(mSceneRootView, R.layout.scene_change_image_transform_end, mContext);
     ```

   * Fade,Slide,Explode
      这三个都是根据view的visibility的不同分别创建渐入，滑动，爆炸动画。

   同时，也可以通过XML来创建动画，对于动画的集合来说XML会更加方便

   **res/transition/changebounds_and_fade.xml**:

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <transitionSet xmlns:android="http://schemas.android.com/apk/res/android">
   <changeBounds />
   <fade />
   </transitionSet>
   ```

   ```java
   Transition sets=TransitionInflater.from(this).inflateTransition(R.transition.changebounds_and_fade);
   ```

   Last: TransitionManager.go(scene2)其实是调用当前的scene(scene1)的scene1.exit()以及下一个scene(scene2)的scene2.enter(),而他们又会出发scene1.setExitAction()和scene1.setEnterAction()，可以在这两个方法中制定一些特别的效果。

3. **beginDelayedTransition()**

   `TransitionManager.go()`都是通过XML文件创造的start scene和 end scene来操作的，而`beginDelayedTransition()`原理是通过代码改变view的属性，然后通过上面的动画类分析start scene和 end scene不同来创建动画。

   ```java
   @Override
   public void onClick(View v) {
       //start scene 是当前的scene
     TransitionManager.beginDelayedTransition(sceneRoot, TransitionInflater.from(this).inflateTransition(R.transition.explode_and_changebounds));
       //next scene 此时通过代码已改变了scene statue
     changeScene(v);
   }
   
   private void changeScene(View view) {
       changeSize(view);
       changeVisibility(cuteboy,cutegirl,hxy,lly);
       view.setVisibility(View.VISIBLE);
   }
   
   /**
    * view的宽高1.5倍和原尺寸大小切换 * 配合ChangeBounds实现缩放效果 * @param view
     */
   private void changeSize(View view) {
       isImageBigger=!isImageBigger;
       ViewGroup.LayoutParams layoutParams = view.getLayoutParams();
       if(isImageBigger){
           layoutParams.width=(int)(1.5*primarySize);
           layoutParams.height=(int)(1.5*primarySize);
       }else {
           layoutParams.width=primarySize;
           layoutParams.height=primarySize;
       }
       view.setLayoutParams(layoutParams);
   }
   
   /**
    * VISIBLE和INVISIBLE状态切换 * @param views
     */
   private void changeVisibility(View ...views){
       for (View view:views){
           view.setVisibility(view.getVisibility()==View.VISIBLE?View.INVISIBLE:View.VISIBLE);
       }
   }
   
   ```

4. **界面切换动画**

   Activity/Fragment之间的切换动画效果，界面切换有两种，一种是不带共享元素的Content Transition 一种是带有共享元素的Shared Element Transition

   1. **Content Transition**

      A.startActivity(B)

      - A.exitTransition(transition)

        Transition框架会先遍历A界面确定要执行动画的view(非共享元素view)，执行`A.exitTransition()`前A界面会获取界面的start scene(view 处于VISIBLE状态)，然后将所有的要执行动画的view设置为INVISIBLE，并获取此时的end scene(view 处于INVISIBLE状态).根据transition分析差异的不同创建执行动画。

      - B.enterTransition()

        Transition框架会先遍历B界面，确定要执行动画的view，设置为INVISIBLE。执行`B.enterTransition()`前获取此时的start scene(view 处于INVISIBLE状态)，然后将所有的要执行动画的view设置为VISIBLE，并获取此时的end scene(view 处于VISIBLE状态).根据transition分析差异的不同创建执行动画。

      - 根据以上说明界面切换动画是建立在visibility的改变的基础上的，所以getWindow().setEnterTransition(transition);中的参数一般传的是Fade, Slide, Explode类的实例（因为这三个类是通过分析visiblity不同创建动画的），通常写一个完整的Activity Content Transition有以下几个步骤：

        1. 在style中添加， Material主题的应用自动设置为true

           ```xml
           <item name="android:windowActivityTransitions">true</item>
           ```

        2. 设置相应的A离开/B进入/B离开/A重新进入动画。

           ```java
           //A 不设置默认为null
           getWindow().setExitTransition(transition);
           //B 不设置默认为Fade
           getWindow().setEnterTransition(transition);
           //B 不设置默认为EnterTransition
           getWindow().setReturnTransition(transition);
           //A 不设置默认为ExitTransition
           getWindow().setReenterTransition(transition);
           
           ```

           也可以在主题中设定

           ``` xml
           <item name="android:windowEnterTransition">@transition/slide_and_fade</item>
           <item name="android:windowReturnTransition">@transition/return_slide</item>
           
           ```

        3. 跳转界面

        4. ```java
           ActivityOptions compat = ActivityOptions.makeCustomAnimation(mContext, R.anim.top_in, R.anim.bottom_out);
           startActivity(new Intent(mContext, MakeCustomerAnimationActivity.class), compat.toBundle());
           ```

           但你会发现，在界面切换的时候，A退出时，过了一小会，B就进入了，如果想等A完全退出后B再进入可以通过设置`setAllowEnterTransitionOverlap(false)`,同样也可以通过XML设置

           ``` xml
           <item name="android:windowAllowEnterTransitionOverlap">false</item>
           <item name="android:windowAllowReturnTransitionOverlap">false</item>
           ```

           仔细看的时候A的状态栏也跟着下啦上拉了，所以需要Transition框架只关注某一个view或者不关注某一个view，这时候就需要transition.addTarget()和transition.excludeTarget()，也可以在XML中设置该属性。

           ```xml
           <transitionSet xmlns:android="http://schemas.android.com/apk/res/android">
           <slide android:duration="1000">
               <targets >
                   <!--表示除了状态栏-->
                   <target android:excludeId="@android:id/statusBarBackground"/>
                   <!--表示只针对状态栏-->
            <!--<target android:targetId="@android:id/statusBarBackground"/>-->  </targets>
           </slide>
           </transitionSet>
           ```
