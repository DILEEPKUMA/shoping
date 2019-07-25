@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    data = request.get_json()
    shop_db = db.shop_details
    if current_user.is_authenticated():
        flash('You are already logged in.')
        return redirect(index_url_for_blueprint(current_user))
    data = ForgotPassworddata()
    if data.validate_on_submit():
        user = User.query.filter_by(email=data.email.data).first()
        if user:
            send_reset_email(user = user)
            flash('The password reset email was sent.')
            # return redirect(url_for('.index'))
        data.email.errors.append('Your email is invalid.')
    return render_template('hello', data=data)


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    if current_user.is_authenticated():
        flash('You are already logged in.')
        return redirect(index_url_for_blueprint(current_user))
    user = User.query.filter_by(reset_token = token).first()
    if user is None:
        return abort(404)
    data = ResetPassworddata()
    if data.validate_on_submit():
        user.set_password(data.new_password.data)
        flash('Your password was successfully changed.')
        login_user(user)
        user.reset_token = None
        return redirect(index_url_for_blueprint(current_user))        
    return render_template('main/reset_password.html', data=data)


@app.route('/forget_password', methods=['GET','POST'])
def forget_password():
    if request.method == 'GET':
        data = request.get_json()
        shop_db = db.shop_details
        # login_username = shop_db.find_one({'shop_email': data['shop_email']})
        cursor = shop_db.find_one({'shop_email': data['shop_email']})
        shop_email=data['shop_email']
        for doc in cursor:
            if shop_email == data['shop_email']:
                print("mail is avaible")
            print(doc)
