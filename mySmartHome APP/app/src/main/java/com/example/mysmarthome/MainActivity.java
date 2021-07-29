package com.example.mysmarthome;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.time.Duration;
import java.time.LocalTime;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private FirebaseStorage storage ;
    private StorageReference storageReference;
    FirebaseDatabase database;





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Global.main = MainActivity.this;
        storage = FirebaseStorage.getInstance();
        storageReference = storage.getReference();
        Global.storageReference= storageReference;




    }

    @Override
    public void onStart() {
        super.onStart();
        database = FirebaseDatabase.getInstance();
        LocalTime now = LocalTime.now();

        DatabaseReference myRef1 = database.getReference("notification");

        myRef1.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for(DataSnapshot ds : dataSnapshot.getChildren()) {
                    String notification = ds.child("notification").getValue(String.class);
                    Log.d("TAG2", notification );

                    if(notification.equals("yes") && Global.systemwork &&!Global.Guestname.equals("") &&  Duration.between(now,Global.time).toMinutes() <1){

                        Button b3 = findViewById(R.id.button3);
                        b3.setVisibility(View.VISIBLE);

                    }

                }
            }


            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Log.w("x", "Failed to read value.", error.toException());

            }

        });










        DatabaseReference myRef = database.getReference("system");

        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for(DataSnapshot ds : dataSnapshot.getChildren()) {
                    String state = ds.child("state").getValue(String.class);
                    if(state.equals("close")){
                        Button bsystem = (Button) findViewById(R.id.button5);
                        bsystem.setVisibility(View.VISIBLE);
                        TextView tsystem = (TextView) findViewById(R.id.textView2);
                        tsystem.setVisibility(View.VISIBLE);
                        Global.systemwork= false;
                        Button b3 = findViewById(R.id.button3);
                        b3.setVisibility(View.INVISIBLE);
                        Button b10 = findViewById(R.id.button10);
                        b10.setVisibility(View.INVISIBLE);


                        Button b11 = findViewById(R.id.button11);
                        b11.setVisibility(View.VISIBLE);


                    }
                    else{
                        Button bsystem = (Button) findViewById(R.id.button5);
                        bsystem.setVisibility(View.INVISIBLE);
                        TextView tsystem = (TextView) findViewById(R.id.textView2);
                        tsystem.setVisibility(View.INVISIBLE);
                        Global.systemwork= true;
                        Button b10 = findViewById(R.id.button10);
                        b10.setVisibility(View.VISIBLE);
                        Button b11 = findViewById(R.id.button11);
                        b11.setVisibility(View.INVISIBLE);



                    }

                }


            }


            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Log.w("x", "Failed to read value.", error.toException());

            }

        });








    }

public void smarthome(View view){
    Intent i  = new Intent(this, MainActivity3.class);
    startActivity(i);
}

public void Log(View view){
    Intent i  = new Intent(this, MainActivity4.class);
    startActivity(i);


}
public void turnoff(View view){
    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference myRef = database.getReference("appsystem");
    myRef.setValue("systemOff");
    Global.systemwork= false;

}
    public void turnon(View view){
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference("appsystem");
        myRef.setValue("systemOn");
        Global.systemwork= true;
        Global.Guestname="";


    }


public void homeowners(View view){
    Intent i = new Intent(this, MainActivity5.class);
    startActivity(i);
}
}
