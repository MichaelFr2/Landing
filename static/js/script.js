
var enjoyhint_instance = new EnjoyHint({});

var options = [
    {
        "next #Ga" : '<br>QUACK! Here are some tips - move next!',
        showSkip:false

    },
    {
    "next #work-exp" : 'You can change needed working experience',
    showSkip:false
    },

    {'next #edu' : 'Try to change the level of education!',
    showSkip:false
    },

    {'next #stack' : 'Here you can control stack-choosing options',
    showSkip:false
    },
    {'next #s-skills' : 'Add here your soft skills',
    showSkip:false
    },

    {'next #languages' : 'Write here your other languages',
    showSkip:false
    },

    {'next #comment' : 'You can write an additional comment if you need!',
    showSkip:false
    },
    {'next #confirm' : 'After all changes are made - confirm by nod!',
    showSkip:false,
    },
    {
        "next #Ga" : '<br>Well, now you are ready to try the service!',
        'nextButton' : {text: "Finish!"},
        showSkip:false,
    }

]

enjoyhint_instance.set(options);
enjoyhint_instance.run();