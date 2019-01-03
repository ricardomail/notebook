1. Android 系统每隔16ms发出VSYNC信号触发对UI的渲染，要求每一帧都要在16ms内处理完成
2. UI丢帧原因有： layout太过复杂，层次过多，过度绘制， CPU或GPU负载过重，动画执行次数过多，频繁GC，UI线程执行耗时操作
3. Linearlayout在measure的时候，在横向或者纵向只会测量一次，但设置layout_weight的时候会测量两遍
4. RelativeLayout在measure的时候会横向纵向各测量一遍
5. 优化：避免使用复杂的view层级， 避免layout顶层使用RelativeLayout，布局层次相同的情况下使用LinearLayout， 复杂布局建议采用RelativeLayout而不是多层LinearLayout，<include/>标签复用，<merge/>标签减少嵌套，避免使用layout_weight，视图按需加载使用ViewStub

### stubview

1. 一个轻量级的view，没有尺寸 ，不绘制任何东西，因此绘制或者移除时更省时

2. 实现view的延迟加载，避免资源浪费，减少渲染时间

3. * viewstub所要替代的layout文件中不能有`<merge>` 标签
   * viewstub在加载完后会被移除，或者说是被加载进来的layout替换掉了

4. ```xml
   <ViewStub
       android:id="@+id/stub_import"
       android:inflatedId="@+id/panel_import"
       android:layout="@layout/progress_overlay"
       android:layout_width="fill_parent"
       android:layout_height="wrap_content"
       android:layout_gravity="bottom" />
   
   ```

5. 用viewstub加载layout文件时，可以调用`setVisibility(View.VISIBLE)`或者`inflate()`

6. ```java
   @Override
       public void onClick(View v) {
           switch (v.getId()) {
               case R.id.btn_vs_showView:
   
                   //inflate 方法只能被调用一次，因为调用后viewStub对象就被移除了视图树；
                   // 所以，如果此时再次点击显示按钮，就会崩溃，错误信息：ViewStub must have a non-null ViewGroup viewParent；
                   // 所以使用try catch ,当此处发现exception 的时候，在catch中使用setVisibility()重新显示
                   try {
                       View iv_vsContent = viewStub.inflate();     //inflate 方法只能被调用一次，
                       hintText = (TextView) iv_vsContent.findViewById(R.id.tv_vsContent);
                       //                    hintText.setText("没有相关数据，请刷新");
                   } catch (Exception e) {
                       viewStub.setVisibility(View.VISIBLE);
                   } finally {
                       hintText.setText("没有相关数据，请刷新");
                   }
                   break;
               case R.id.btn_vs_hideView:  //如果显示
                   viewStub.setVisibility(View.INVISIBLE);
                   break;
               case R.id.btn_vs_changeHint:
                   if (hintText!=null) { 
                       hintText.setText("网络异常，无法刷新，请检查网络");
                   }
                   break;
           }
   
   ```

7. viewstub的`inflate()`只能被调用一次

