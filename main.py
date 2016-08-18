#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi


html_head = """
<!DOCTYPE html>
    <html>
    <head>
        <title>
            Rot13 Exercise JH
        </title>
    </head>
    <body>
    <h1>
    Welcome to the Encrypter!
    </h1>

"""
html_tail = """
<p> this is the end </p>
</body>
</html>
"""

rotation_form = """
    <form method = "post">
        <label for = "rotNum"> How much would you like to rotate by? </label>
        <input type = "text" name = "rotNum" value = "%(rotNum)s">
        <br>
        %(phrase)s
        <br>
        <textarea type = "text" name = "test"
            style="height:150px; width:450px">
        %(test)s
        </textarea>
        <br>
        <input type = "submit">
    </form>
    """

#rotate character function
def rotate_character(char, rot):
    """rotates a given character to another value by a given rotation amount"""
    #find new position in alphabet
    listLower = "abcdefghijklmnopqrstuvwxyz"
    listUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if char.isalpha():
        if char.islower():
            i = listLower.index(char)
            newPosition = (i + rot)%26
            newChar = listLower[newPosition]
        if char.isupper():
            i = listUpper.index(char)
            newPosition = (i + rot)%26
            newChar = listUpper[newPosition]
    else:
        newChar= char
    return newChar

#Caesar cipher
def caesar_encrypt(text, rot):
    """uses rotate_character to encrypt a given text by a given rotation"""
    encrypted_text = ''
    for i in text:
        encrypted_text = encrypted_text + rotate_character(i, rot)
    return encrypted_text









class MainHandler(webapp2.RequestHandler):
    def write_form(self, phrase="", test="", rotNum=""):
        self.response.write(html_head + rotation_form % {"test":test, "rotNum":rotNum, "phrase":phrase} + html_tail)

    def get(self):
        get_phrase = "What phrase should we encrypt for you?"
        self.write_form(get_phrase)

    def post(self):
        user_text = self.request.get('test')
        user_num = int(self.request.get('rotNum'))
        user_encrypted = caesar_encrypt(user_text, user_num)
        #escape text for html use
        user_encrypted = cgi.escape(user_encrypted, quote = True)
        response_phrase = "Here is your encrypted text:"

        self.write_form(response_phrase, user_encrypted, user_num)







app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
