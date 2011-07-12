from django.db import models
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.files import File

from zipfile import ZipFile
from shutil import copyfile
import os
import datetime

class Edition(models.Model):
    date = models.DateField(unique=True)
    output = models.FileField(upload_to='output')
    pdf = models.FileField(upload_to='pdf', editable=False)
    
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return self.date.strftime("%Y-%m-%d")
    
    def save(self, *args, **kwargs):
        if not self.pdf:
            # output path
            output_path = os.path.join(settings.MEDIA_ROOT, 'output')
            
            # empty the output directory
            for entity in os.listdir(output_path):
                file_path = os.path.join(output_path, entity)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            # initial save
            super(Edition, self).save(*args, **kwargs)
            
            # open zip, extract and close
            zip = ZipFile(self.output.path)
            zip.extractall(output_path)
            zip.close()
            
            # take pdf file
            pdf_file = File(open(os.path.join(output_path, 'file.pdf'), 'rb'))
            
            # save pdf file and edition object
            self.pdf.save(
                self.date.strftime("%Y-%m-%d.pdf"),
                pdf_file
            )
            pdf_file.close()
            
            # remove pdf file from output path
            os.remove(pdf_file.name)
            
            i = 1
            for entry in os.listdir(output_path):
                if entry.endswith('.txt'):
                    page = Page()
                    page.edition = self
                    
                    page.number = i
                    
                    txt_file = open(os.path.join(output_path, entry))
                    page.text = txt_file.read()
                    txt_file.close()
                    
                    img_file = ImageFile(
                        open(
                            os.path.join(
                                output_path,
                                'scr-%d.png' % (i - 1)
                            ),
                            'rb'
                        )
                    )
                    page.screenshot.save(
                        # self.date.strftime("%Y-%m-%d.png").replace('.png', '-%d.png' % i),
                        self.date.strftime("%Y-%m-%d.png")[:-4] + '-%d.png' % i,
                        img_file
                    )
                    
                    # take pdf file
                    pdf_page_file = File(open(os.path.join(output_path, 'file-%d.pdf' % (i - 1)), 'rb'))
                    
                    # save pdf file and edition object
                    page.pdf.save(
                        # self.date.strftime("%Y-%m-%d.pdf").replace('.pdf', '-%d.pdf' % i),
                        self.date.strftime("%Y-%m-%d.pdf")[:-4] + '-%d.pdf' % i,
                        pdf_page_file
                    )
                    pdf_page_file.close()
                        
                    
                    i = i + 1
                
                # remove processed file
                file_path = os.path.join(output_path, entry)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                # print os.path.join(output_path, entry)
        else:
            # super(Edition, self).save(*args, **kwargs)
            pass
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