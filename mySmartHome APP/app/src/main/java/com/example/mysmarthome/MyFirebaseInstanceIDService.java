package com.example.mysmarthome;

import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.util.Log;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

import java.time.LocalTime;

import androidx.annotation.NonNull;


public class MyFirebaseInstanceIDService extends FirebaseMessagingService {
    @Override
    public void onCreate() {
        super.onCreate();

        }





    @Override
    public void onNewToken(@NonNull String s) {
        super.onNewToken(s);
        Log.d("kero",s);
    }

    @Override
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        super.onMessageReceived(remoteMessage);
        if(remoteMessage.getData().get("imgnamex") != null){
            Log.d("msg", remoteMessage.getData().get("imgnamex"));
            Global.Guestname= remoteMessage.getData().get("imgnamex");
            Global.time = LocalTime.now();
            try {
                Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
                Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
                r.play();
            } catch (Exception e) {
                e.printStackTrace();
            }



        }
        else {
            if (remoteMessage.getData().get("imgname") != null) {
                Log.d("msg", remoteMessage.getData().get("imgname"));
                Global.Guestname = remoteMessage.getData().get("imgname");
                Global.time = LocalTime.now();
            }
        }








    }





}
