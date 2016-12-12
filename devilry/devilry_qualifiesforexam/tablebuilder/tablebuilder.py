# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Devilry imports
from devilry.devilry_cradmin.devilry_tablebuilder import base as tablebuilderbase


class QualifiesTableBuilderTable(tablebuilderbase.Table):
    @classmethod
    def from_qualifying_items(cls, row_items_list, **kwargs):
        """

        Args:
            row_items_list: This must be a list of row data lists.
                Example with relatedstudents and their qualification status::
                    [
                        [relatedstudent1, qualifies, ...],
                        [relatedstudent2, qualifies, ...]
                    ]

        Note:
            If you want to customize each cell independently you have to know exactly
            how many elements in each row and in what order of course to be able to customize them.

        Returns:
            Instance of :class:`~.devilry.devilry_cradmin.devilry_tablebuilder.base.Table`.

        """
        header_row = QualificationRowRenderer()
        header_row.extend([
            QualificationHeaderRenderer(value='Student'),
            QualificationHeaderRenderer(value='Qualified for final exams')
        ])
        tablebuilder_table = cls(table_headers=header_row)
        for row_items in row_items_list:
            row_renderer = QualificationRowRenderer()
            row_renderer.extend([
                QualificationStudentInfoCellRenderer(value=row_items[0]),
                QualificationStatusCellRenderer(value=row_items[1])
            ])
            fr = QualificationFrameRenderer(inneritem=row_renderer)
            tablebuilder_table.append(row_renderer=fr)
        return tablebuilder_table

    def get_extra_css_classes_list(self):
        css_list = super(QualifiesTableBuilderTable, self).get_extra_css_classes_list()
        css_list.append('devilry-qualifiesforexam-table')
        return css_list


class QualificationFrameRenderer(tablebuilderbase.ItemFrameRenderer):
    def get_extra_css_classes_list(self):
        # print 'frame'
        css_classes_list = super(QualificationFrameRenderer, self).get_extra_css_classes_list()
        css_classes_list.append('devilry-qualifiesforexam-row-hover')
        return css_classes_list


class QualificationRowRenderer(tablebuilderbase.RowRenderer):
    def get_extra_css_classes_list(self):
        css_classes_list = super(QualificationRowRenderer, self).get_extra_css_classes_list()
        css_classes_list.append('devilry-qualifiesforexam-tr')
        return css_classes_list


class QualificationHeaderRenderer(tablebuilderbase.ColumnHeaderRenderer):
    template_name = 'devilry_qualifiesforexam/tablebuilder/tableheader_valueitem.django.html'
    valuealias = 'header_description'

    def get_extra_css_classes_list(self):
        css_classes_list = super(QualificationHeaderRenderer, self).get_extra_css_classes_list()
        css_classes_list.append('devilry-qualifiesforexam-th')
        return css_classes_list


class QualificationStudentInfoCellRenderer(tablebuilderbase.ColumnItemRenderer):
    template_name = 'devilry_qualifiesforexam/tablebuilder/relatedstudent_valueitem.django.html'
    valuealias = 'relatedstudent'

    def get_extra_css_classes_list(self):
        css_classes_list = super(QualificationStudentInfoCellRenderer, self).get_extra_css_classes_list()
        css_classes_list.append('devilry-qualifiesforexam-cell-studentinfo')
        return css_classes_list


class QualificationStatusCellRenderer(tablebuilderbase.ColumnItemRenderer):
    template_name = 'devilry_qualifiesforexam/tablebuilder/qualificationstatus_valueitem.django.html'
    valuealias = 'result'

    def get_extra_css_classes_list(self):
        css_classes_list = super(QualificationStatusCellRenderer, self).get_extra_css_classes_list()
        css_classes_list.append('devilry-qualifiesforexam-cell-qualify')
        return css_classes_list
