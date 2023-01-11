server {
    listen 8443;
    server_name https://chatbot.talentpowered.team;

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/home/goose/goose.sock;
    }
}