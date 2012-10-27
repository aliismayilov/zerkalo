from django.db import models
from django.core.files import File
from django.core.files.images import ImageFile
from django.conf import settings

from libs.pdf_tools import *

import os


class Edition(models.Model):
    date = models.DateField(unique=True)
    pdf = models.FileField(upload_to='pdf')
    
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return self.date.strftime("%Y-%m-%d")
    
    def save(self, *args, **kwargs):
        # initial save
        super(Edition, self).save(*args, **kwargs)
        
        # rename actual filename on filesystem
        os.rename(
            self.pdf._get_path(),
            self.pdf._get_path().replace(
                os.path.basename(self.pdf._get_path()), os.path.basename(self.date.strftime('%Y-%m-%d.pdf'))
            )
        )
        
        # rename pdf in edition object
        self.pdf.name = 'pdf/' + self.date.strftime('%Y-%m-%d.pdf')
    
        # save with new filename
        super(Edition, self).save(*args, **kwargs)
        
        # output directory to keep files in purpose for not duplicate, yes, I speak very good English
        output_directory = os.path.join(settings.MEDIA_ROOT, 'output')
        
        # xml file where we keep character dictionary
        chars_xml_filename = os.path.join(settings.MEDIA_ROOT, 'chars.xml')
        
        # split pdf to pages and return pdf filenames
        page_filenames = pdf_split(self.pdf._get_path(), output_directory)
        
        # forloop counter
        i = 1
        
        # create pages
        for page_filename in page_filenames:
            # create new page
            page = Page()
            page.edition = self
            page.number = i
            
            # extract pdf text
            page.text = extract_text(page_filename, chars_xml_filename)
            
            # attach pdf file page
            page.pdf.save(
                self.date.strftime("%Y-%m-%d.pdf")[:-4] + "-%d.pdf" % i, 
                File(open(page_filename, 'rb')),
                save=False
            )
            
            # remove duplicate file
            os.remove(page_filename)
            
            # full path to screenshot directory
            scr_directory = os.path.join(settings.MEDIA_ROOT, 'scr')
            
            # generate pdf screenshot and get its filename
            scr_filename = pdf_screenshot(
                page.pdf._get_path(),
                os.path.join(output_directory, self.date.strftime("%Y-%m-%d.png")[:-4] + "-%d.png" % i)
            )
            
            # attach screenshot to page and save
            page.screenshot.save(
                self.date.strftime("%Y-%m-%d.png")[:-4] + "-%d.png" % i,
                ImageFile(open(scr_filename, 'rb')),
            )
            
            # remove duplicate file
            os.remove(scr_filename)
            
            i += 1
        
    def get_absolute_url(self):
        return "/%s" % self.date.strftime("%Y-%m-%d")

class Page(models.Model):
    edition = models.ForeignKey(Edition)
    screenshot = models.ImageField(upload_to='scr')
    pdf = models.FileField(upload_to='pdf')
    number = models.IntegerField() # page number
    text = models.TextField()
    
    def get_absolute_url(self):
        return self.screenshot.url


class Chapter(models.Model):
    name = models.CharField(max_length=50)
    page_number = models.IntegerField()
    edition = models.ForeignKey(Edition)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['page_number']