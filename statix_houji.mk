#
# Copyright (c) 2014 The Android Open-Source Project
# Copyright (c) 2024 StatiXOS
#
# SPDX-License-Identifier: Apache-2.0
# 
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base.mk)
$(call inherit-product, device/xiaomi/houji/device.mk)

PRODUCT_NAME := statix_houji
PRODUCT_DEVICE := houji
PRODUCT_BRAND := xiaomi
PRODUCT_MODEL := houji
PRODUCT_MANUFACTURER := xiaomi
