
package com.example.mysmarthome;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.time.Duration;
import java.time.LocalTime;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity3 extends AppCompatActivity {

    FirebaseDatabase database;



    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main3);
        database = FirebaseDatabase.getInstance();

    }
    public void onStart() {
        super.onStart();
        LocalTime now = LocalTime.now();

        DatabaseReference myRef1 = database.getReference("notification");

        myRef1.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for(DataSnapshot ds : dataSnapshot.getChildren()) {
                    String notification = ds.child("notification").getValue(String.class);
                    Log.d("TAG22", notification );

                    if(notification.equals("yes") && Global.systemwork &&!Global.Guestname.equals("") &&  Duration.between(now,Global.time).toMinutes() <1){

                        Button b3 =(Button) findViewById(R.id.button3);
                        b3.setVisibility(View.VISIBLE);

                    }
                    else{
                        Button b3 = findViewById(R.id.button3);
                        b3.setVisibility(View.INVISIBLE);

                    }

                }
            }




            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Log.w("table", "Failed to read value.", error.toException());

            }

        });








    }


    public void check(View view){
        if(Global.systemwork) {
            Intent i = new Intent(this, MainActivity2.class);
            startActivity(i);
        }
        else{
            Toast.makeText(this,"system is turned off!" , Toast.LENGTH_SHORT).show();

        }

    }

    public void open(View view){
        if(Global.systemwork) {
            Global.Guestname = "";
            Global.time = null;
            Button btemp = (Button) Global.main.findViewById(R.id.button3);
            btemp.setVisibility(View.INVISIBLE);


            Button b3 = findViewById(R.id.button3);
            b3.setVisibility(View.INVISIBLE);

            FirebaseDatabase database = FirebaseDatabase.getInstance();
            DatabaseReference myRef = database.getReference("smartdoor");
            myRef.setValue("open");
            Toast.makeText(this,"Opening door is processing" , Toast.LENGTH_LONG).show();



        }
        else{
            Toast.makeText(this,"system is turned off!" , Toast.LENGTH_SHORT).show();
        }
    }

    public void close(View view){
        if(Global.systemwork) {
                Global.Guestname = "";
                Global.time= null;
                Button btemp = (Button)Global.main.findViewById(R.id.button3);
                btemp.setVisibility(View.INVISIBLE);


                Button b3 = findViewById(R.id.button3);
                b3.setVisibility(View.INVISIBLE);


                FirebaseDatabase database = FirebaseDatabase.getInstance();
                DatabaseReference myRef = database.getReference("smartdoor");
                myRef.setValue("close");
                Toast.makeText(this,"Closing door is processing" , Toast.LENGTH_LONG).show();


        }
        else{
            Toast.makeText(this,"system is turned off!" ,Toast.LENGTH_SHORT).show();
        }


    }


}