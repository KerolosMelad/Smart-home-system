package com.example.mysmarthome;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.StorageReference;

import java.time.Duration;
import java.time.LocalTime;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity2 extends AppCompatActivity {
    ImageView rImage ;
    TextView tv;
    TextView tv2;
    FirebaseDatabase database;
    static boolean  flag = true;



    @Override
    protected void onCreate(Bundle savedInstanceState) {


        super.onCreate(savedInstanceState);
        database = FirebaseDatabase.getInstance();
        setContentView(R.layout.activity_main2);




    }

    @Override
    protected void onStart() {
        super.onStart();
        LocalTime now = LocalTime.now();

        DatabaseReference myRef1 = database.getReference("notification");

        myRef1.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for(DataSnapshot ds : dataSnapshot.getChildren()) {
                    String notification = ds.child("notification").getValue(String.class);


                    if(notification.equals("yes") && Global.systemwork &&!Global.Guestname.equals("") &&  Duration.between(now,Global.time).toMinutes() <1){

                        flag = false;
                        tv2 = findViewById(R.id.textView3);
                        tv2.setVisibility(View.VISIBLE);
                        StorageReference getImage = Global.storageReference.child(Global.Guestname);
                        tv = findViewById(R.id.textView);
                        tv.setVisibility(View.INVISIBLE);



                        long maxbytes = 1024 * 1024;
                        getImage.getBytes(maxbytes).addOnSuccessListener(new OnSuccessListener<byte[]>() {
                            @Override
                            public void onSuccess(byte[] bytes) {

                                Bitmap bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                                rImage = findViewById(R.id.imageView2);
                                rImage.setImageBitmap(bitmap);
                                tv2.setVisibility(View.INVISIBLE);
                                rImage.setVisibility(View.VISIBLE);


                            }
                        });

                    }
                    else{

                            if(rImage != null) {
                                rImage.setVisibility(View.INVISIBLE);
                            }
                            tv = findViewById(R.id.textView);
                            tv.setVisibility(View.VISIBLE);


                    }

                }
            }




            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Log.w("table", "Failed to read value.", error.toException());

            }

        });



        if(flag && Global.systemwork &&!Global.Guestname.equals("") &&  Duration.between(now,Global.time).toMinutes() <1){

            tv2 = findViewById(R.id.textView3);
            tv2.setVisibility(View.VISIBLE);
            StorageReference getImage = Global.storageReference.child(Global.Guestname);
            tv = findViewById(R.id.textView);
            tv.setVisibility(View.INVISIBLE);



            long maxbytes = 1024 * 1024;
            getImage.getBytes(maxbytes).addOnSuccessListener(new OnSuccessListener<byte[]>() {
                @Override
                public void onSuccess(byte[] bytes) {

                    Bitmap bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                    rImage = findViewById(R.id.imageView2);
                    rImage.setImageBitmap(bitmap);
                    tv2.setVisibility(View.INVISIBLE);
                    rImage.setVisibility(View.VISIBLE);


                }
            });

        }
        else{

            if(rImage != null) {
                rImage.setVisibility(View.INVISIBLE);
            }
            tv = findViewById(R.id.textView);
            tv.setVisibility(View.VISIBLE);


        }




    }
}


