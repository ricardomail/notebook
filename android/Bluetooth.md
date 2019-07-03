https://www.cnblogs.com/xxzjyf/p/x_x_z_j_y_f.html

#### Android Ble

1. 低功耗蓝牙 数据传输速率低，快速链接，用于可穿戴设备之中
2. profile可以理解为一种规范，标准的通信协议，每个profile中包含了多个service
3. service可以理解为一个服务，在BLE从机中有多个服务，电量信息，系统服务信息等，每一个service中包含多个characteristic特征值
4. BLE主机从机通信均是通过characteristic进行，通过该标签可以读取或者写入相关信息
5. UUID service和characteristic都需要这个唯一的UUID进行标示

#### 编码

1. 权限 

   ```java
   <uses-featureandroid:name="android.hardware.bluetooth_le"android:required="true"/>
   
   <uses-permissionandroid:name="android.permission.BLUETOOTH"/>
   
   <uses-permissionandroid:name="android.permission.BLUETOOTH_ADMIN"/>
   ```

2. 初始化蓝牙

   ```java
   BluetoothManager mBluetoothManager = (BluetoothManager) this.getSystemService(Context.BLUETOOTH_SERVICE);
                if (mBluetoothManager != null) {
                          BluetoothAdapter mBluetoothAdapter = mBluetoothManager.getAdapter();
                              if (mBluetoothAdapter != null) {
                                        if (!mBluetoothAdapter.isEnabled()) {
                                             mBluetoothAdapter.enable();  //打开蓝牙
                                }
                        }
                  }
   ```

3. 获取本地BLE对象（BluetoothAdapter）

   ```java
   BluetoothManager bluetoothManager = (BluetoothManager) context.getSystemService(Context.BLUETOOTH_SERVICE);  //BluetoothManager只在android4.3以上有
              if (bluetoothManager == null) {
                          TLog.e(TAG, "Unable to initialize BluetoothManager.");
                           return;
              }
   
             mBluetoothAdapter = bluetoothManager.getAdapter();
   ```

4. 搜索ble设备

   ```java
   mBluetoothAdapter.startLeScan(mLeScanCallback);   //此mLeScanCallback为回调函数
   private LeScanCallback mLeScanCallback = new LeScanCallback() {
       @Override
             public void onLeScan(BluetoothDevice device, int arg1, byte[] arg2) {
                      TLog.i(TAG, "onLeScan() DeviceName------>"+device.getName());  //在这里可通过device这个对象来获取到搜索到的ble设备名称和一些相关信息
                      if(device.getName() == null){  
                              return;
                      }
                     if (device.getName().contains("Ble_Name")) {    //判断是否搜索到你需要的ble设备
                                TLog.i(TAG, "onLeScan() DeviceAddress------>"+device.getAddress());
                                mBluetoothDevice = device;   //获取到周边设备
                                stopLeScan();   //1、当找到对应的设备后，立即停止扫描；2、不要循环搜索设备，为每次搜索设置适合的时间限制。避免设备不在可用范围的时候持续不停扫描，消耗电量。
   
                                connect();  //连接
                    } 
         }
   };
   ```

5. 获取设备之后建立Gatt链接

   ```java
   mBluetoothGatt = mBluetoothDevice.connectGatt(mContext, false, mGattCallback);  //mGattCallback为回调接口
   
   private final BluetoothGattCallback mGattCallback = new BluetoothGattCallback() {
   @Override
   public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
                       if (newState == BluetoothProfile.STATE_CONNECTED) {
                                     gatt.discoverServices(); //执行到这里其实蓝牙已经连接成功了
   
                                     TLog.i(TAG, "Connected to GATT server.");
                              } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                                         if(mBluetoothDevice != null){
                                                 TLog.i(TAG, "重新连接");
                                                       connect();
                                                  }else{
                                                      TLog.i(TAG, "Disconnected from GATT server.");
                             }
                  }
   }
       
   
   public void onServicesDiscovered(BluetoothGatt gatt, int status) {
              if (status == BluetoothGatt.GATT_SUCCESS) {
                   TLog.i(TAG, "onServicesDiscovered");
                   getBatteryLevel();  //获取电量
         } else {
                 TLog.i(TAG, "onServicesDiscovered status------>" + status);
        }
   }
   
   @Override
   public void onCharacteristicRead(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status) {
          TLog.d(TAG, "onCharacteristicRead------>" + Utils.bytesToHexString(characteristic.getValue()));
   
   //判断UUID是否相等
          if (Values.UUID_KEY_BATTERY_LEVEL_CHARACTERISTICS.equals(characteristic.getUuid().toString())) { 
   }
   }
   
   @Override
   public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic) {
         TLog.d(TAG, "onCharacteristicChanged------>" + Utils.bytesToHexString(characteristic.getValue()));
   
   //判断UUID是否相等
         if (Values.UUID_KEY_BATTERY_LEVEL_CHARACTERISTICS.equals(characteristic.getUuid().toString())) {
   }
   }
   
   //接受Characteristic被写的通知,收到蓝牙模块的数据后会触发onCharacteristicWrite
   @Override
   public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status) {
          TLog.d(TAG,"status = " + status);
          TLog.d(TAG, "onCharacteristicWrite------>" + Utils.bytesToHexString(characteristic.getValue()));
   }
   };
   ```

6. 获取服务与特征

   ```java
   public BluetoothGattService getService(UUID uuid) {
   if (mBluetoothAdapter == null || mBluetoothGatt == null) {
   TLog.e(TAG, "BluetoothAdapter not initialized");
   return null;
   }
   return mBluetoothGatt.getService(uuid);
   }
   
   //b.获取特征
   
   private BluetoothGattCharacteristic getCharcteristic(String serviceUUID, String characteristicUUID) {
   
   //得到服务对象
   BluetoothGattService service = getService(UUID.fromString(serviceUUID));  //调用上面获取服务的方法
   
   if (service == null) {
   TLog.e(TAG, "Can not find 'BluetoothGattService'");
   return null;
   }
   
   //得到此服务结点下Characteristic对象
   final BluetoothGattCharacteristic gattCharacteristic = service.getCharacteristic(UUID.fromString(characteristicUUID));
   if (gattCharacteristic != null) {
   return gattCharacteristic;
   } else {
   TLog.e(TAG, "Can not find 'BluetoothGattCharacteristic'");
   return null;
   }
   }
   
   
   ```

7. 写入数据

   ```java
   public void write(byte[] data) {   //一般都是传byte
             //得到可写入的characteristic Utils.isAIRPLANE(mContext) && 
               if(!mBleManager.isEnabled()){
                   TLog.e(TAG, "writeCharacteristic 开启飞行模式");
                   //closeBluetoothGatt();
                   isGattConnected = false;
                   broadcastUpdate(Config.ACTION_GATT_DISCONNECTED);
                   return;
              }
            BluetoothGattCharacteristic writeCharacteristic = getCharcteristic(Values.UUID_KEY_SERVICE, Values.UUID_KEY_WRITE);  //这个UUID都是根据协议号的UUID
            if (writeCharacteristic == null) {
            TLog.e(TAG, "Write failed. GattCharacteristic is null.");
            return;
        }
        writeCharacteristic.setValue(data); //为characteristic赋值
        writeCharacteristicWrite(writeCharacteristic);
   
   }
   ```


