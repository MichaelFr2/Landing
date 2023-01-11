introJs().setOptions({
    steps: [
    {
      title: 'QUACK!',
      intro: 'Here are some tips - move next!',
      element: document.querySelector('.img-header img'),
      hidePrev: true
    
    },
    {
      element: document.querySelector('.work-exp'),
      intro: 'You can change needed working experience'
    },
    {
       element: document.querySelector('.edu'),
       intro: 'Try to change the level of education!'
    },
    {
        element: document.querySelector('.stack'),
        intro: 'Here you can control stack-choosing options'
    },
    {
        element: document.querySelector('.s-skills'),
        intro: 'Add here your soft skills'
    },
    {
        element: document.querySelector('.languages'),
        intro: 'Write here your other languages'
    },
    {
        element: document.querySelector('.comment'),
        intro: 'You can write an additional comment if you need!'
    },
    {
        element: document.querySelector('.btn-sub'),
        intro: 'After all changes are made - confirm by nod!'
    },
    {
        element: document.querySelector('.img-header'),
        intro: 'Well, now you are ready to try the service!'
    }

   ]
  }).start();

// "next #Ga" : '<br>QUACK! Here are some tips - move next!',
// "next #work-exp" : 'You can change needed working experience',
// 'next #edu' : 'Try to change the level of education!'
// 'next #stack' : 'Here you can control stack-choosing options',
// 'next #s-skills' : 'Add here your soft skills',
// 'next #languages' : 'Write here your other languages',
// 'next #comment' : 'You can write an additional comment if you need!',
// 'next #confirm' : 'After all changes are made - confirm by nod!',
// "next #Ga" : '<br>Well, now you are ready to try the service!',