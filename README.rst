======
pylio
======
:Author: Christoforus Surjoputro <cs_sanmar@yahoo.com>
:Date: $Date: 2017-07-04 $
:Version: $Version: 1.0.0 $
:License: MIT License

.. role:: python(code)
   :language: python

.. image:: https://travis-ci.org/rekeninghub/pylio.svg?branch=development
    :target: https://travis-ci.org/rekeninghub/pylio

.. contents:: Table of content

Introduction
============

`pylio`_ is python asynchronous module to access https://helio.id API. In this version, you can only send email.

Python version
--------------

This module work on python 3.5+.

How to install
==============

.. code-block:: bash

    pip install Pylio

How to use
==========

1. Import pylio to your project by doing this :python:`from pylio import PylioAsync`.
2. Setup https://www.mainapi.net token to library by doing this :python:`pylio = PylioAsync('YOUR_MAINAPI_TOKEN')`.
3. Sign in to HELIO mail server and save the token by doing this :python:`pylio.signin('YOUR_EMAIL_ADDRESS', 'YOUR_PASSWORD')`.
4. Send email to any email address.

Send email
----------

You can send email by doing this:

.. code-block:: python

    pylio.send_email('HELIO_SIGNIN_TOKEN', 'EMAIL_ADDRESS_RECIPIENT', 'EMAIL_SUBJECT', 'EMAIL_BODY')

How to contribute
=================

Just create an `issue`_ when you encounter any problem.

.. _`pylio`: https://gitlab.com/rekeninghub/pylio
.. _`issue`: https://gitlab.com/rekeninghub/pylio/issues
