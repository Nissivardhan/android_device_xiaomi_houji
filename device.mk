#
# Copyright (c) 2014 The Android Open-Source Project
# Copyright (c) 2024 StatiXOS
#
# SPDX-License-Identifier: Apache-2.0
#
$(call inherit-product, vendor/xiaomi/houji/houji-vendor.mk)

TARGET_KERNEL_DIR := device/xiaomi/houji-kernel

$(call inherit-product, device/xiaomi/sm8650-common/pineapple.mk)

# Soong
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)
