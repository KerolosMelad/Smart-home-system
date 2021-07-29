package com.example.mysmarthome;

import android.content.ClipData;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity5 extends AppCompatActivity {
    TableLayout tl ;
    FirebaseDatabase database;
    List<Bitmap> bitmaps ;
    private FirebaseStorage storage ;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main5);
        database = FirebaseDatabase.getInstance();

        bitmaps = new ArrayList<>();
        storage = FirebaseStorage.getInstance();


        database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference("homeowners");

        tl = (TableLayout)findViewById(R.id.table);
        tl.setStretchAllColumns(true);
        tl.bringToFront();
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

                tl.removeAllViews();
                TableRow tr = new TableRow(MainActivity5.this);
                TextView c1 = new TextView(MainActivity5.this);
                c1.setText("Home owner");
                c1.setTextColor(Color.rgb(0,0,0));
                tr.addView(c1);
                tl.addView(tr);

                for(DataSnapshot ds : dataSnapshot.getChildren()) {
                    Log.d("TAG", "onDataChange: "+ds.child("name").getValue(String.class));
                    String name = ds.child("name").getValue(String.class);
                    TableRow trx = new TableRow(MainActivity5.this);
                    TextView cx = new TextView(MainActivity5.this);

                    cx.setText(name );
                    trx.addView(cx);
                    tl.addView(trx);



                }

                //  Log.d("table", "Value is: " + dataSnapshot);

            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Log.w("table", "Failed to read value.", error.toException());

            }

        });

    }



    public void addtoDB(View view){
        EditText ex = (EditText) findViewById(R.id.editTextTextPersonName2);
        String username = ex.getText().toString();
        if(username.equals("")){
            Toast.makeText(this,"please enter home owner's name",Toast.LENGTH_SHORT).show();
            return;
        }
        if(!bitmaps.isEmpty()){


            StorageReference storageReference = storage.getReference();
            int counter =0 ;
            TextView tv4= findViewById(R.id.textView4);
            tv4.setVisibility(View.VISIBLE);

            for ( Bitmap image : bitmaps) {
                StorageReference storageRef = storage.getReference();
                StorageReference mountainImagesRef = storageRef.child(counter+".jpg");
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                image.compress(Bitmap.CompressFormat.JPEG, 20, baos);
                byte[] data = baos.toByteArray();
                UploadTask uploadTask = mountainImagesRef.putBytes(data);
                counter++;
            }
            DatabaseReference myRef1 = database.getReference("newUser");
            myRef1.setValue(username);
            DatabaseReference myRef2 = database.getReference("counter");
            myRef2.setValue(counter);
            tv4.setVisibility(View.INVISIBLE);
            ex.setText("");


            if(Global.systemwork){
                Toast.makeText(this,"Kindly, restart the system to add the new user to database",Toast.LENGTH_LONG).show();
            }
            else{
                Toast.makeText(this,"Successfuly added to DB",Toast.LENGTH_LONG).show();

            }

        }
        else{
            Toast.makeText(this,"please select home owner's images",Toast.LENGTH_SHORT).show();
            return;
        }

    }

     public void Gallerybutton(View view){
        if(!bitmaps.isEmpty()) {
            Toast.makeText(this, "The pre-selected images will be deleted", Toast.LENGTH_SHORT).show();
            bitmaps.clear();
        }
         launchGalleryIntent();
    }

    public void launchGalleryIntent() {

        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        intent.setType("image/*");
        startActivityForResult(intent, 100  );
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case 100: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // permission was granted, yay! Do the
                    // contacts-related task you need to do.
                    launchGalleryIntent();
                } else {
                    // permission denied, boo! Disable the
                    // functionality that depends on this permission.
                }
                return;
            }

            // other 'case' lines to check for other
            // permissions this app might request.
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable  Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 100
                && resultCode == RESULT_OK) {

            ClipData clipData = data.getClipData();

            if (clipData != null) {
                //multiple images selecetd
                Toast.makeText(this,"You have selected " +clipData.getItemCount()+" images" ,Toast.LENGTH_SHORT).show();
                for (int i = 0; i < clipData.getItemCount(); i++) {
                    Uri imageUri = clipData.getItemAt(i).getUri();
                    Log.d("URI", imageUri.toString());
                    try {
                        InputStream inputStream = getContentResolver().openInputStream(imageUri);
                        Bitmap bitmap = BitmapFactory.decodeStream(inputStream);
                        bitmaps.add(bitmap);
                    } catch (FileNotFoundException e) {
                        e.printStackTrace();
                    }
                }
            } else {
                //single image selected
                Uri imageUri = data.getData();
                Log.d("URI", imageUri.toString());
                try {
                    InputStream inputStream = getContentResolver().openInputStream(imageUri);
                    Bitmap bitmap = BitmapFactory.decodeStream(inputStream);
                    bitmaps.add(bitmap);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }

            }


        }
    }
}
