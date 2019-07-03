#### Parcelable

```java
/**
 * Created by ricardo
 * 2019/1/5.
 */
public class Fruit implements Parcelable {
    private String name;
    private int age;


    public static final Creator<Fruit> CREATOR = new Creator<Fruit>() {
        @Override
        public Fruit createFromParcel(Parcel in) {
            Fruit fruit = new Fruit();
            fruit.name = in.readString();
            fruit.age = in.readInt();
            return fruit;

        }

        @Override
        public Fruit[] newArray(int size) {
            return new Fruit[size];
        }
    };

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeString(name);
        parcel.writeInt(age);
    }
}
```





Intent传值接收时用`getParcelableExtra()`方法





#### 定时任务AlarmManager

```java
AlarmManager manager = (AlarmManager) getSystemService(Context.ALARM_SERVICE);
        
        long triggerAtTime = SystemClock.elapsedRealtime() + 10 * 1000;
        manager.set(AlarmManager.ELAPSED_REALTIME_WAKEUP, triggerAtTime, new PendingIntent());
```

PendingIntent()可以从Broadcast或service中获取

SystemClock.elapsedRealtime()获取的是系统开机至今所经历的时间的毫秒值

System.currentTimeMillis()获取到1970年1月1日0点至今所经历的时间的毫秒值

RTC是指1970。REALTIME是指开机，带WAKEUP指的是会唤醒CPU







#### Doze模式

1. 当用户设备是6.0系统以上时，如果该设备未插电源，处于静止（7.0删掉了这一条件），且屏幕关闭了一段时间之后，会进入Doze模式，进入后会对CPU,网络，Alarm等活动进行限制，延长电池使用寿命
2. * 网络访问被禁止
   * 系统忽略唤醒CPU或者屏幕操作
   * 系统不再进行WIFI扫描
   * 不再执行同步服务
   * Alarm任务会在下次退出Doze模式的时候执行
3. 如果有非常特殊的需求，Alarm在Doze模式下也必须正常执行，调用AlarmManager的`setAndAllowWhileIdle`或者`setExactAndAllowWhileIdle()`方法就可以





#### 多窗口模式

1. 正常app都可以使用多窗口模式
2. 如果不想使用，在manifest文件中配置application或者activity中的`android:resizeableActivity=["true"|"false"]` true代表支持多窗口，默认为true
3. 生命周期：如果处于多窗口状态点击当前，另一个会进入onPause()状态
4. 进入多窗口时会从走生命周期
5. targetSDK23时，单一一个属性置顶非多窗口不好用的，需要在指定activity的`android:screenOrientation="portrait">`属性，稳妥