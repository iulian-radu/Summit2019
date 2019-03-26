# Sample script that generates a test company
This is a fragment of the script that we've used to provision the sites for L743: Optimize Campaigns with Algorithmic Modeling and Audience Lab.

The purpose of the code is to familiarize you with the way you could automate trait/model creation.

## How to invoke
```
python provision.py pid user password client_id client_secret destination_id

```

Parameter details:
* pid - Partner ID. You get this from the consultant that create the account
* user - your user name
* password - your user password
* client_id - Oauth2 client id - For details on how to get this, check here: [https://marketing.adobe.com/resources/help/en_US/aam/oauth-authentication.html](https://marketing.adobe.com/resources/help/en_US/aam/oauth-authentication.html)
* client_secret - Oauth2 client secret - same as above. Get this from your Partner Solutions manager
* destination_id - the id for the batch destination that we'll use for Audience Lab

