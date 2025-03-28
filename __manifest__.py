# -*- coding: utf-8 -*-

{
    "name": "Employee training tracker",
    "version": "0.1",
    "author": "Tri Duc Nguyen",
    "description": "streamline and automate the company's training management process",
    "depends": ["calendar"],
    "data": [
        'security/training_tracker_security.xml',
        'security/ir.model.access.csv',

        'data/training_course_category_data.xml',

        'views/training_course_views.xml',
        'views/training_session_views.xml',
        'views/training_completion_views.xml',
    ],
    "view": "",
    "installable": True,
    "application": True,
}