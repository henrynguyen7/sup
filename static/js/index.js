/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
var app = {
    // Application Constructor
    initialize: function() {
        this.bindEvents();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function() {
        document.addEventListener("deviceready", this.onDeviceReady, false);
    },
    // Process any received events.
    receivedEvent: function(id) {
        console.log("Received Event: " + id);
    },
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicity call 'app.receivedEvent(...);'
    onDeviceReady: function() {
        app.receivedEvent("deviceready");
    },
    onLoginPage: function() {

        var form = document.getElementById("form_login");
        var preference = window.plugins.appPreferences;

        if (form !== undefined && form !== null) {

            if (preference.fetch(app.onPreferenceSuccess, app.onPreferenceFailure, "password") !== "" &&
                preference.fetch(app.onPreferenceSuccess, app.onPreferenceFailure, "password") !== undefined) {

                form.elements["username"].value = preference.fetch(app.onPreferenceSuccess, app.onPreferenceFailure, "username");
                form.elements["password"].value = preference.fetch(app.onPreferenceSuccess, app.onPreferenceFailure, "password");
                form.submit();

            } else {

                if (form.attachEvent) {
                    form.attachEvent("submit", app.savePreferences);
                } else {
                    form.addEventListener("submit", app.savePreferences);
                }
            }
        }
    },
    savePreferences: function(e) {
        var form = document.getElementById("form_login");
        var preference = window.plugins.appPreferences;
        preference.store(app.onPreferenceSuccess, app.onPreferenceFailure, "username", form.elements["username"].value);
        preference.store(app.onPreferenceSuccess, app.onPreferenceFailure, "password", form.elements["password"].value);
    },
    onPreferenceSuccess: function(result) {
        console.log("onPreferenceSuccess! Result = " + result);
    },
    onPreferenceFailure: function(error) {
        console.log("onPreferenceFailure! Error = " + error);
    },
    onPushSuccess: function(result) {
        console.log("onPushSuccess! Result = " + result);
    },
    onPushFailure: function(error) {
        console.log("onPushFailure! Error = " + error);
    },
    onNotificationGCM: function(e) {

        switch (e.event) {

            case "registered":

                if (e.regid.length > 0) {

                    if (device.platform == "Android") {
                        window.app.gcm_id = e.regid;
                    } else if (device.platform == "iOS") {
                        window.app.apn_id = e.regid;
                    }

                    var form = document.getElementById("form_registration");
                    var inputGcmId = document.createElement("input");
                    var inputDevicePlatform = document.createElement("input");

                    inputGcmId.type = "hidden";
                    inputGcmId.name = "gcm_id";
                    inputGcmId.value = window.app.gcm_id;

                    inputDevicePlatform.type = "hidden";
                    inputDevicePlatform.name = "device_platform";
                    inputDevicePlatform.value = device.platform;

                    form.appendChild(inputGcmId);
                    form.appendChild(inputDevicePlatform);
                    form.submit();
                }
                break;

            case "message":
                // this is the actual push notification. its format depends on the data model from the push server
                alert(e.message);
                break;

            case "error":
                alert("GCM error = " + e.msg);
                break;

            default:
                alert("An unknown GCM event has occurred");
                break;
        }
    }
};
