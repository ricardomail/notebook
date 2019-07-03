#### 滑动菜单

#### DrawerLayout:

```xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.v4.widget.DrawerLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/drawer"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MaterialActivity">

    <android.support.design.widget.CoordinatorLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        <android.support.design.widget.AppBarLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content">
            <android.support.v7.widget.Toolbar
                android:id="@+id/toolbar"
                android:layout_width="match_parent"
                android:layout_height="?attr/actionBarSize"
                android:background="@color/colorPrimary"
                app:title="Hello"
                app:titleTextColor="#fff"
                android:theme="@style/ThemeOverlay.AppCompat.Dark.ActionBar"
                app:popupTheme="@style/ThemeOverlay.AppCompat.Light"
                app:layout_scrollFlags="enterAlways|scroll|snap"/>
        </android.support.design.widget.AppBarLayout>

        <android.support.v7.widget.RecyclerView
            android:id="@+id/recycle"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            app:layout_behavior="@string/appbar_scrolling_view_behavior"/>
        <android.support.design.widget.FloatingActionButton
            android:id="@+id/floatbtn"
            android:layout_gravity="bottom|right"
            android:layout_margin="16dp"
            android:src="@drawable/ic_menu"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:backgroundTint="#ffffff"
            app:borderWidth="0dp"/>


    </android.support.design.widget.CoordinatorLayout>
    <TextView
        android:id="@+id/tv"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_gravity="start"
        android:textSize="20sp"
        android:background="#fff"
        />
</android.support.v4.widget.DrawerLayout>
```

DrawerLayout可以作为画面的根布局，其中包含两个子布局，一个是主画面的布局，还有一个是侧滑菜单的布局，侧滑菜单的布局一般使用NavigationView来做，侧滑布局要加入android:layout_gravity="start"，可以让侧滑从左侧出现，也可以在toolbar上加按钮控制开启和关闭

```java
toolbar = (Toolbar) findViewById(R.id.toolbar);
        // 报错是因为导错了包
        setSupportActionBar(toolbar);
        mDraw = (DrawerLayout) findViewById(R.id.drawer);
        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null){
            // 让导航按钮显示出来
            actionBar.setDisplayHomeAsUpEnabled(true);
            // 设置导航按钮图标
            actionBar.setHomeAsUpIndicator(R.drawable.ic_menu);
        }
        
@Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case android.R.id.home:
                // 导航按钮的点击事件。需要传入GravityCompat.START
                mDraw.openDrawer(GravityCompat.START);
                break;
        }
        return true;
    }
```



#### NavigationView

1. 在design包中
2. 需要提前准备好headerLayout和menu
3. setCheckedItem(int Id). 指定初始默认



#### FloatingActionButton

1. 悬浮按钮

2. Layout_gravity指定在屏幕位置

3. elevation属性决定投影范围，越大，投影范围越大，投影效果越淡

4. android:backgroundTint="#ffffff" 指定按钮背景，默认为系统主题颜色

5. borderwidth设置按钮边距，防止有颜色边

6. app:layout_anchor="@id/app_bar"锚点属性

7. 点击事件：

   ```java
   fBtn.setOnClickListener(new View.OnClickListener() {
               @Override
               public void onClick(View view) {
                   Snackbar.make(view, "Data deleted", Snackbar.LENGTH_SHORT)
                           .setAction("undo", new View.OnClickListener() {
                               @Override
                               public void onClick(View view) {
                                   Toast.makeText(MaterialActivity.this, "restored", Toast.LENGTH_SHORT).show();
                               }
                           }).show();
               }
           });
   ```





#### Snackbar

```java
Snackbar.make(view, "Data deleted", Snackbar.LENGTH_SHORT)
        .setAction("undo", new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(MaterialActivity.this, "restored", Toast.LENGTH_SHORT).show();
            }
        }).show();
```

1. 和coordinatorLayout结合起来防止把FloatingActionButton遮挡

   ```xml
   <android.support.design.widget.CoordinatorLayout
           android:layout_width="match_parent"
           android:layout_height="match_parent">
           <android.support.design.widget.AppBarLayout
               android:layout_width="match_parent"
               android:layout_height="wrap_content">
               <android.support.v7.widget.Toolbar
                   android:id="@+id/toolbar"
                   android:layout_width="match_parent"
                   android:layout_height="?attr/actionBarSize"
                   android:background="@color/colorPrimary"
                   app:title="Hello"
                   app:titleTextColor="#fff"
                   android:theme="@style/ThemeOverlay.AppCompat.Dark.ActionBar"
                   app:popupTheme="@style/ThemeOverlay.AppCompat.Light"
                   app:layout_scrollFlags="enterAlways|scroll|snap"/>
           </android.support.design.widget.AppBarLayout>
   
           <android.support.v7.widget.RecyclerView
               android:id="@+id/recycle"
               android:layout_width="match_parent"
               android:layout_height="match_parent"
               app:layout_behavior="@string/appbar_scrolling_view_behavior"/>
           <android.support.design.widget.FloatingActionButton
               android:id="@+id/floatbtn"
               android:layout_gravity="bottom|right"
               android:layout_margin="16dp"
               android:src="@drawable/ic_menu"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:backgroundTint="#ffffff"
               app:borderWidth="0dp"/>
   
   
       </android.support.design.widget.CoordinatorLayout>
   ```

2. CoordinatorLayout相当于一个加强版的FrameLayout





#### AppBarLayout

1. 正常情况下CoordinateLayout中的RecycleView会把Toolbar遮挡，因为是一个FrameLayout，此时就需要这个布局，实际上它是一个垂直的LinearLayout，首先将Toolbar嵌入到Appbar中，然后给RecycleView增加一个行为属性。 搞定

```xml
<android.support.design.widget.CoordinatorLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        <android.support.design.widget.AppBarLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content">
            <android.support.v7.widget.Toolbar
                android:id="@+id/toolbar"
                android:layout_width="match_parent"
                android:layout_height="?attr/actionBarSize"
                android:background="@color/colorPrimary"
                app:title="Hello"
                app:titleTextColor="#fff"
                android:theme="@style/ThemeOverlay.AppCompat.Dark.ActionBar"
                app:popupTheme="@style/ThemeOverlay.AppCompat.Light"
                app:layout_scrollFlags="enterAlways|scroll|snap"/>
        </android.support.design.widget.AppBarLayout>

        <android.support.v7.widget.RecyclerView
            android:id="@+id/recycle"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            app:layout_behavior="@string/appbar_scrolling_view_behavior"/>
        <android.support.design.widget.FloatingActionButton
            android:id="@+id/floatbtn"
            android:layout_gravity="bottom|right"
            android:layout_margin="16dp"
            android:src="@drawable/ic_menu"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:backgroundTint="#ffffff"
            app:borderWidth="0dp"/>


    </android.support.design.widget.CoordinatorLayout>

```

AppBar只能是CoordinatorLayout的子布局



#### CollapsingToolbarLayout

1. 只能作为AppBar的子布局
2. app:contentScrim="?attr/colorPrimary"用来指定折叠后的toolbar颜色
3. app:layout_collapseMode="pin"属性表示折叠模式， pin表示位置不变，parallax表示会产生一定的错位偏移
4. 