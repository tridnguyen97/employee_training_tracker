# -*- coding: utf-8 -*-

from odoo import fields, models


class CourseCategory(models.Model):
    _name = "training.course.category"
    _description = "Training Course Category"
    _parent_store = True
    _parent_name = "parent_id"

    name = fields.Char(string="Category Name", required=True)
    description = fields.Text(string="Description")
    parent_id = fields.Many2one("training.course.category", string="Parent Category",
                                ondelete="restrict")
    child_ids = fields.One2many("training.course.category", "parent_id",
                                string="Child Categories")
    parent_path = fields.Char(index=True) # needed for _parent_store
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(string="Sequence", default=10)
    course_ids = fields.One2many('training.course', 'category_id', string="Courses") # Relation to the course model.

    _sql_constraints = [
        ('name_uniq', 'unique(name, parent_id)', 'Category name must be unique within its parent category.'),
    ]
