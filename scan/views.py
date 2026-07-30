import io
import qrcode
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from assets.models import Asset


def asset_detail(request, asset_tag):
    asset = get_object_or_404(Asset, asset_tag=asset_tag)
    context = {
        'asset': asset,
        'specs': asset.specs.all(),
        'documents': asset.documents.filter(is_public=True),
    }
    return render(request, 'scan/asset_detail.html', context)

def asset_qr(request, asset_tag):
    asset = get_object_or_404(Asset, asset_tag=asset_tag)
    url = request.build_absolute_uri(f'/a/{asset.asset_tag}/')
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def asset_label(request, asset_tag):
    asset = get_object_or_404(Asset, asset_tag=asset_tag)
    return render(request, 'scan/asset_label.html', {'asset': asset})