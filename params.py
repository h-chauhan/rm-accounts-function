getParams = lambda type: {
    'loginUrl': 'http://tnp.dtu.ac.in/rm_2016-17/intern/intern_login',
    'username_field': 'intern_student_username_rollnumber',
    'password_field': 'intern_student_password',
    'notifsUrl': 'http://tnp.dtu.ac.in/rm_2016-17/intern/intern_student',
    'year': '2K16'
} if type == 'internship' else {
    'loginUrl': 'http://tnp.dtu.ac.in/rm_2016-17/login',
    'username_field': 'student_username_rollnumber',
    'password_field': 'student_password',
    'notifsUrl': 'http://tnp.dtu.ac.in/rm_2016-17/student',
    'year': '2K15'
}
