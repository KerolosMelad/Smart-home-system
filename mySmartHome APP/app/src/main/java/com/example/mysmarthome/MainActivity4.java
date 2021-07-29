package com.example.mysmarthome;

import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity4 extends AppCompatActivity {
    TableLayout tl ;
    FirebaseDatabase database;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main4);

        database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference("log");

        tl = (TableLayout)findViewById(R.id.table);
        tl.setStretchAllColumns(true);
        tl.bringToFront();
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                tl.removeAllViews();
                TableRow tr = new TableRow(MainActivity4.this);
                TextView c1 = new TextView(MainActivity4.this);
                c1.setText("persons/s" +"                    " +"action" + "                        " + "time");
                c1.setTextColor(Color.rgb(0,0,0));
                tr.addView(c1);
                tl.addView(tr);

                for(DataSnapshot ds : dataSnapshot.getChildren()) {

                    String name = ds.child("person").getValue(String.class);
                    String time = ds.child("time").getValue(String.class);
                    String action = ds.child("action").getValue(String.class);
                    TableRow trx = new TableRow(MainActivity4.this);
                    TextView cx = new TextView(MainActivity4.this);
                    String space = "          ";
                    String space2 = "       ";

                    if(action.length()>17)
                        space = "  ";
                    else
                        space2 +="     ";
                    cx.setText(name +space +action + space2 + time);
                    trx.addView(cx);
                    tl.addView(trx);






                    Log.d("table", "Value is: " + name +action + time );

                }

                //  Log.d("table", "Value is: " + dataSnapshot);

            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Log.w("table", "Failed to read value.", error.toException());

            }

        });

    }
    public void clearlog(View view){
        DatabaseReference myRef = database.getReference("log");
        myRef.removeValue();


    }
}