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
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'odm/lib64/hw/camera.qcom.so',
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so')
        # MiuiCamera 2x (tele): SensorNode::ExecuteProcessRequest crashes on a NULL
        # client-name (strcmp(NULL, "com.android.camera")) under AOSP. Replace that
        # `bl strcmp` with `mov w0, #0` so it takes the MIUI SAT path -> 2x works.
        .binary_regex_replace(
            b'\xd4\x12\x09\x94',  # bl strcmp
            b'\x00\x00\x80\x52',  # mov w0, #0
        ),
    (
        'odm/lib64/com.qti.feature2.gs.sm8650.so',
    ): blob_fixup()
        # General-stats feature graph: type-7 map dispatch — force the b.hi error
        # branch (@0xa1e78) to take case0 instead of erroring out.
        .binary_regex_replace(
            b'\x3f\x16\x00\x71\xc8\x07\x00\x54',  # cmp w17,#5 ; b.hi error
            b'\x3f\x16\x00\x71\x28\x0e\x00\x54',  # cmp w17,#5 ; b.hi case0
        ),
    (
        'odm/lib64/camera/components/com.xiaomi.node.smooth_transition.so',
    ): blob_fixup()
        # SupportedFeature descriptor numUnits: 1 -> 2 (struct @0x216e0, name ptr
        # to "SupportedFeature" @vaddr 0x224f).
        .binary_regex_replace(
            b'\x4f\x22\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00',
            b'\x4f\x22\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00',
        ),
    (
        'odm/lib64/hw/com.qti.chi.override.so',
    ): blob_fixup()
        # aeRegion + afRegion numUnits: 4 -> 5 (two descriptors @0x5728a8/0x5728c8).
        .binary_regex_replace(
            b'\x94\x11\x0a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00',  # aeRegion
            b'\x94\x11\x0a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00',
        )
        .binary_regex_replace(
            b'\x6b\x7b\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00',  # afRegion
            b'\x6b\x7b\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00',
        ),
    (
        'odm/lib64/libchifeature2.so',
    ): blob_fixup()
        # aeRegion + afRegion numUnits: 4 -> 5 (two descriptors @0x5728a8/0x5728c8).
        .binary_regex_replace(
            b'\x84\x11\x0a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00',  # aeRegion
            b'\x84\x11\x0a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00',
        )
        .binary_regex_replace(
            b'\x5b\x7b\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00',  # afRegion
            b'\x5b\x7b\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00',
        ),
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