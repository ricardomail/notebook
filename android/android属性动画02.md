#### TypeEvaluator

* **ArgbEvaluator**: 用来做颜色的渐变

  ```java
  ObjectAnimator animator = ObjectAnimator.ofInt(view, "color", 0xffff0000, 0xff00ff00);  
  animator.setEvaluator(new ArgbEvaluator());  
  animator.start();  
  ```

  如果当前minsdk版本大于21，也可以用ofArgb来实现：

  ```java
  ObjectAnimator animator = ObjectAnimator.ofArgb(view, "color", 0xffff0000, 0xff00ff00);  
  animator.start();  
  ```

* **ofObject()**: 可以不限定类型做动画

  ```java
  private class PointFEvaluator implements TypeEvaluator<PointF> {  
     PointF newPoint = new PointF();
  
     @Override
     public PointF evaluate(float fraction, PointF startValue, PointF endValue) {
         float x = startValue.x + (fraction * (endValue.x - startValue.x));
         float y = startValue.y + (fraction * (endValue.y - startValue.y));
  
         newPoint.set(x, y);
  
         return newPoint;
     }
  }
  
  ObjectAnimator animator = ObjectAnimator.ofObject(view, "position",  
          new PointFEvaluator(), new PointF(0, 0), new PointF(1, 1));
  animator.start();  
  ```

* **PropertyValuesHolder**：ObjectAnimator中用于同一动画改变多个属性

  ```java
  PropertyValuesHolder holder1 = PropertyValuesHolder.ofFloat("scaleX", 1);  
  PropertyValuesHolder holder2 = PropertyValuesHolder.ofFloat("scaleY", 1);  
  PropertyValuesHolder holder3 = PropertyValuesHolder.ofFloat("alpha", 1);
  
  ObjectAnimator animator = ObjectAnimator.ofPropertyValuesHolder(view, holder1, holder2, holder3)  
  animator.start(); 
  ```

* **AnimatorSet**: 多个动画配合执行

  ```Java
  ObjectAnimator animator1 = ObjectAnimator.ofFloat(view, "alpha", 0, 1);
  ObjectAnimator animator2 = ObjectAnimator.ofFloat(view, "translationX", -200, 200);
  ObjectAnimator animator3 = ObjectAnimator.ofFloat(view, "rotation", 0, 1080);
  animator3.setDuration(1000);
  
  AnimatorSet animatorSet = new AnimatorSet();
  // 用 AnimatorSet 的方法来让三个动画协作执行
  // 要求 1： animator1 先执行，animator2 在 animator1 完成后立即开始
  animatorSet.play(animator1).before(animator2);
  // 要求 2： animator2 和 animator3 同时开始
  animatorSet.play(animator2).with(animator3);
  
  animatorSet.start();
  ```

  ```java
  animatorSet.playSequentially(animator1, animator2); //两个动画依次执行
  ```

  ```java
  // 两个动画同时执行
  animatorSet.playTogether(animator1, animator2); 
  ```

* **PropertyValuesHolders.ofKeyframe()**: 把同一个属性拆分

  ```java
  // 在 0% 处开始
  Keyframe keyframe1 = Keyframe.ofFloat(0, 0);  
  // 时间经过 50% 的时候，动画完成度 100%
  Keyframe keyframe2 = Keyframe.ofFloat(0.5f, 100);  
  // 时间见过 100% 的时候，动画完成度倒退到 80%，即反弹 20%
  Keyframe keyframe3 = Keyframe.ofFloat(1, 80);  
  PropertyValuesHolder holder = PropertyValuesHolder.ofKeyframe("progress", keyframe1, keyframe2, keyframe3);
  
  ObjectAnimator animator = ObjectAnimator.ofPropertyValuesHolder(view, holder);  
  animator.start();
  ```


