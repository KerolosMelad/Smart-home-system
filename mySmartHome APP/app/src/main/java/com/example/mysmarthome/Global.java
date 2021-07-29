package com.example.mysmarthome;

import android.app.Activity;

import com.google.firebase.storage.StorageReference;

import java.time.LocalTime;

public class Global {
    public static String Guestname ="";
    public static LocalTime time ;
    public static StorageReference storageReference;
    public static int rows = 0 ;
    public static Activity main ;
    public static boolean systemwork = false;
}
