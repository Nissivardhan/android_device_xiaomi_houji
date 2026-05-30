#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sm8650-common',
    'hardware/qcom-caf/sm8650',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/xiaomi/sm8650-common',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    'libcameraopt': lib_fixup_vendor_suffix,
    (
        'android.hardware.graphics.composer3-V1-ndk',
        'android.hardware.graphics.allocator-V1-ndk',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'odm/lib64/hw/camera.xiaomi.so',
        'odm/lib64/com.xiaomi.camhal.overlap.so',
        'odm/lib64/com.xiaomi.camhal.submodel.camxfrag.so',
        'odm/lib64/com.xiaomi.camhal.submodel.chifrag.so',
        'odm/lib64/libcom.xiaomi.ecoenginemonitor.so',
        'odm/lib64/libcom.xiaomi.grallocutils.so',
        'odm/lib64/libcom.xiaomi.mawutils.so',
        'odm/lib64/libcom.xiaomi.mawutilsold.so',
        'odm/lib64/libecoengine.so',
        'odm/lib64/libmialgoengine.so',
        'odm/lib64/libmis_plugin_his.so',
        'odm/lib64/libmorpho_video_stabilizer.so',
        'odm/lib64/camera/components/com.jigan.node.videobokeh.so',
        'odm/lib64/camera/components/com.mi.node.aiasd.so',
        'odm/lib64/camera/components/com.mi.node.facealign.so',
        'odm/lib64/camera/components/com.mi.node.mawcommon.so',
        'odm/lib64/camera/components/com.mi.node.skinbeautifier.so',
        'odm/lib64/camera/components/com.mi.node.tsskinbeautifier.so',
        'odm/lib64/camera/components/com.mi.node.videobokeh.so',
        'odm/lib64/camera/components/com.mi.node.videofilter.so',
        'odm/lib64/camera/components/com.mi.node.videonight.so',
        'odm/lib64/camera/components/com.qti.node.dewarp.so',
        'odm/lib64/camera/components/com.qti.node.intelligentfocus.so',
        'odm/lib64/camera/components/com.xiaomi.node.gme.so',
        'odm/lib64/camera/components/com.xiaomi.node.misv2.so',
        'odm/lib64/camera/components/com.xiaomi.node.misv3.so',
        'odm/lib64/camera/plugins/com.xiaomi.plugin.arcsoftportraitsll.so',
        'odm/lib64/camera/plugins/com.xiaomi.plugin.arcsofttfsll.so',
        'odm/lib64/camera/plugins/com.xiaomi.plugin.beautydeformation.so',
        'odm/lib64/camera/plugins/com.xiaomi.plugin.mawaiie.so',
        'odm/lib64/camera/plugins/com.xiaomi.plugin.mialgoellc.so',
        'odm/lib64/camera/plugins/com.xiaomi.plugin.tsskinbeautifier.so',
        'vendor/lib64/libqvrcamera_client.qti.so',
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-service.so',
    ): blob_fixup()
        .replace_needed('libui.so', 'libui-34.so'),
    (
        'odm/etc/camera/enhance_motiontuning.xml',
        'odm/etc/camera/night_motiontuning.xml',
        'odm/etc/camera/motiontuning.xml'
    ): blob_fixup()
        .regex_replace('xml=version', 'xml version'),
    (
        'odm/lib64/libcamxcommonutils.so',
        'vendor/lib64/libcameraopt.so',
        'odm/lib64/hw/camera.qcom.so'
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
}

module = ExtractUtilsModule(
    'houji',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm8650-common', module.vendor
    )
    utils.run()