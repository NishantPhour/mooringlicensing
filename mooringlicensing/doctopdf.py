import os

from django.conf import settings
from docxtpl import DocxTemplate
from mooringlicensing.components.main.models import GlobalSettings


def create_dcv_permit_pdf_bytes(dcv_permit):

    licence_template = GlobalSettings.objects.get(key=GlobalSettings.KEY_DCV_PERMIT_TEMPLATE_FILE)

    if licence_template._file:
        path_to_template = licence_template._file.path
    else:
        raise Exception('DcvPermit template file not found.')

    doc = DocxTemplate(path_to_template)
    
    context = dcv_permit.get_context_for_licence_permit()
    if 'p_address_line2' in context and context['p_address_line2'] is None:
        context['p_address_line2'] = '' 
    doc.render(context)

    temp_directory = settings.BASE_DIR + "/tmp/"
    try:
        os.stat(temp_directory)
    except:
        os.mkdir(temp_directory)

    f_name = temp_directory + 'dcv_permit_' + str(dcv_permit.id)
    new_doc_file = f_name + '.docx'
    new_pdf_file = f_name + '.pdf'
    doc.save(new_doc_file)
    os.system("libreoffice --headless --convert-to pdf " + new_doc_file + " --outdir " + temp_directory)

    file_contents = None
    with open(new_pdf_file, 'rb') as f:
        file_contents = f.read()
    os.remove(new_doc_file)
    os.remove(new_pdf_file)
    return file_contents


def create_dcv_admission_pdf_bytes(dcv_admission_arrival):
    licence_template = GlobalSettings.objects.get(key=GlobalSettings.KEY_DCV_ADMISSION_TEMPLATE_FILE)

    if licence_template._file:
        path_to_template = licence_template._file.path
    else:
        raise Exception('DcvAdmission template file not found.')

    doc = DocxTemplate(path_to_template)

    context = dcv_admission_arrival.get_context_for_licence_permit()
    doc.render(context)

    temp_directory = settings.BASE_DIR + "/tmp/"
    try:
        os.stat(temp_directory)
    except:
        os.mkdir(temp_directory)

    f_name = temp_directory + 'dcv_admission' + str(dcv_admission_arrival.dcv_admission.id)
    new_doc_file = f_name + '.docx'
    new_pdf_file = f_name + '.pdf'
    doc.save(new_doc_file)
    os.system("libreoffice --headless --convert-to pdf " + new_doc_file + " --outdir " + temp_directory)

    file_contents = None
    with open(new_pdf_file, 'rb') as f:
        file_contents = f.read()
    os.remove(new_doc_file)
    os.remove(new_pdf_file)
    return file_contents


def create_authorised_user_summary_doc_bytes(approval):
    from mooringlicensing.components.approvals.models import Approval

    # Retrieve a template according to the approval type
    licence_template = GlobalSettings.objects.get(key=GlobalSettings.KEY_ML_AU_LIST_TEMPLATE_FILE)
    if licence_template._file:
        path_to_template = licence_template._file.path
    else:
        raise Exception('Template file not found for {}.'.format(licence_template))

    # Rendering
    doc = DocxTemplate(path_to_template)
    context = approval.child_obj.get_context_for_au_summary() if type(approval) == Approval else approval.get_context_for_au_summary()
    doc.render(context)

    temp_directory = settings.BASE_DIR + "/tmp/"
    try:
        os.stat(temp_directory)
    except:
        os.mkdir(temp_directory)

    f_name = temp_directory + 'approval' + str(approval.id)
    new_doc_file = f_name + '.docx'
    new_pdf_file = f_name + '.pdf'
    doc.save(new_doc_file)
    os.system("libreoffice --headless --convert-to pdf " + new_doc_file + " --outdir " + temp_directory)

    with open(new_pdf_file, 'rb') as f:
        file_contents = f.read()
    os.remove(new_doc_file)
    os.remove(new_pdf_file)
    return file_contents


def create_approval_doc_bytes(approval):
    from mooringlicensing.components.approvals.models import Approval

    # Retrieve a template according to the approval type
    global_setting_key = approval.child_obj.template_file_key if type(approval) == Approval else approval.template_file_key
    licence_template = GlobalSettings.objects.get(key=global_setting_key)
    if licence_template._file:
        path_to_template = licence_template._file.path
    else:
        raise Exception('Template file not found for {}.'.format(licence_template))

    # Rendering
    doc = DocxTemplate(path_to_template)

    context = approval.child_obj.get_context_for_licence_permit() if type(approval) == Approval else approval.get_context_for_licence_permit()
    if 'p_address_line2' in context and context['p_address_line2'] is None:
        context['p_address_line2'] = ''
    doc.render(context)

    temp_directory = settings.BASE_DIR + "/tmp/"
    try:
        os.stat(temp_directory)
    except:
        os.mkdir(temp_directory)

    f_name = temp_directory + 'approval' + str(approval.id)
    new_doc_file = f_name + '.docx'
    new_pdf_file = f_name + '.pdf'
    doc.save(new_doc_file)
    os.system("libreoffice --headless --convert-to pdf " + new_doc_file + " --outdir " + temp_directory)

    with open(new_pdf_file, 'rb') as f:
        file_contents = f.read()
    os.remove(new_doc_file)
    os.remove(new_pdf_file)
    return file_contents