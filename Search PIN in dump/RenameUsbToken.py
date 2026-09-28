# -*- coding: utf-8 -*-
# RenameUsbToken.py
# Names and entry points for the usb_token RP2040 dump.
# The flash block must already be mapped at 0x10000000.
# Image base may be 0. Do not "Set Image Base" or every address shifts.
#
# Run from CodeBrowser:
#   Window -> Script Manager -> Manage Script Directories
#   add the folder that contains THIS file (the file name must be RenameUsbToken.py)
#   select RenameUsbToken.py -> Run
# Then filter Symbol Tree for "main" or "tud_msc".
# Do not decompile boot2_w25q080: that was FUN_10000000 and the bad-instruction warning.
#
# @category RP2040
# @runtime Jython


from java.math import BigInteger
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.lang import RegisterValue


BASE = 0x10000000




def A(off):
    return toAddr(off)




def mem_has(addr):
    return currentProgram.getMemory().contains(addr)




def log(msg):
    println(msg)




def set_thumb_and_disasm(addr):
    if not mem_has(addr):
        log("  missing address %s" % addr)
        return False
    reg = currentProgram.getLanguage().getRegister("TMode")
    cmd = DisassembleCommand(addr, None, True)
    if reg is not None:
        cmd.setInitialContext(RegisterValue(reg, BigInteger.ONE))
    ok = cmd.applyTo(currentProgram, monitor)
    if not ok:
        log("  disasm failed %s : %s" % (addr, cmd.getStatusMsg()))
    return ok




def clear_range(start_off, end_off):
    start = A(start_off)
    end = A(end_off)
    if not mem_has(start):
        return
    addr = start
    seen = set()
    while addr is not None and addr.compareTo(end) <= 0:
        fn = getFunctionContaining(addr)
        if fn is not None:
            key = str(fn.getEntryPoint())
            if key not in seen:
                seen.add(key)
                log("  removeFunction %s" % fn.getName())
                removeFunction(fn)
        addr = addr.add(2)
    clearListing(start, end)




def define_dwords(start_off, count, name=None):
    addr = A(start_off)
    if not mem_has(addr):
        return
    if name:
        try_label(start_off, name, None)
    i = 0
    while i < count:
        a = addr.add(i * 4)
        try:
            createData(a, DWordDataType())
        except Exception, e:
            log("  dword %s: %s" % (a, e))
        i += 1




def try_label(off, name, comment):
    addr = A(off)
    if not mem_has(addr):
        log("  skip label %s (not in image)" % name)
        return
    try:
        createLabel(addr, name, True)
    except Exception:
        pass
    if comment:
        try:
            setPlateComment(addr, comment)
        except Exception, e:
            log("  comment %s: %s" % (name, e))




def ensure_func(off, name, comment=None):
    addr = A(off)
    if not mem_has(addr):
        log("  skip %s" % name)
        return
    containing = getFunctionContaining(addr)
    if containing is not None and not containing.getEntryPoint().equals(addr):
        log("  split %s off %s" % (name, containing.getName()))
        removeFunction(containing)
    existing = getFunctionAt(addr)
    if existing is None:
        set_thumb_and_disasm(addr)
        existing = getFunctionAt(addr)
        if existing is None:
            existing = createFunction(addr, None)
    if existing is None:
        try_label(off, name, comment)
        log("  LABEL only %s" % name)
        return
    existing.setName(name, SourceType.USER_DEFINED)
    if comment:
        existing.setComment(comment)
    log("  %s @ %s" % (name, addr))




def fix_header():
    log("== vector table / binary_info ==")
    # boot2 must not fall into the vector table, or the decompiler
    # reports "Control flow encountered bad instruction data".
    boot = getFunctionAt(A(0x10000000))
    if boot is not None:
        removeFunction(boot)
    clear_range(0x10000100, 0x100001E7)
    define_dwords(0x10000100, 48, "vector_table")
    try_label(0x10000100, "vector_table",
              "SP, Reset, exceptions, IRQs. Low bit of a handler address means Thumb.\n"
              "Reset = 0x100001F7 -> code at 0x100001F6.\n"
              "Almost every IRQ points at isr_default (0x100001C1).")
    define_dwords(0x100001D4, 5, "binary_info_header")
    try_label(0x100001D4, "binary_info_header",
              "0x7188EBF2, bi_start, bi_end, copy_table, 0xE71AA390")


    set_thumb_and_disasm(A(0x10000000))
    set_thumb_and_disasm(A(0x100001C0))
    set_thumb_and_disasm(A(0x100001E8))
    set_thumb_and_disasm(A(0x100001F6))


    ensure_func(0x10000000, "boot2_w25q080",
                "Second-stage bootloader, 256 bytes. Sets up QSPI and jumps to 0x10000100. Not the application.")
    ensure_func(0x100001C0, "isr_default",
                "Unhandled IRQ: mrs IPSR, bkpt. Real USB/GPIO handlers are installed at runtime via VTOR in RAM.")
    ensure_func(0x100001E8, "core1_wait_bootrom",
                "Core 1 sets VTOR=0 and returns to the bootrom. Only core 0 continues.")
    ensure_func(0x100001F6, "reset_handler",
                "crt0: copy .data, zero BSS, blx runtime_init, blx main, blx exit.")




# (address, name, comment)
# Names come from call sites and constants, not from a guess.
FUNCS = [
    (0x10000232, "crt0_copy_words", "Copy .data as (src, dst, dst_end) triples."),
    (0x10000288, "runtime_init_array", "Walks an empty constructor array."),
    (0x100002B0, "dummy_preinit", "Constructor stub. Function pointer is NULL, falls into runtime_init_array."),
    (0x100002E0, "tud_event_noop", "Empty USB callback (bx lr)."),
    (0x100002E4, "tud_msc_test_unit_ready_cb", "Always true. The disk is ready immediately."),
    (0x100002E8, "tud_msc_inquiry_cb", "SCSI Inquiry: vendor POSILABS, product ' FLASH MSC     ', rev '1.0 '."),
    (0x10000340, "tud_msc_capacity_cb", "2048 blocks x 512 bytes = 1 MiB. Second half of flash."),
    (0x10000350, "tud_msc_is_writable_cb", "Always true. Caller derives the MODE SENSE write-protect bit from this."),
    (0x10000354, "tud_msc_read10_cb", "Reads 0x10100000+lba*512 and XORs the sector before returning it to the host."),
    (0x1000053C, "tud_msc_write10_cb", "XOR again, then erase+program a 4K page from SRAM. Interrupts disabled."),
    (0x10000894, "tud_msc_scsi_cb", "Unknown SCSI command: returns -1 so the stack handles it."),
    (0x1000089C, "main", "gpio25, empty stub, lock_ui (blocks), usb init, then tud_task + led_chase."),
    (0x100008C4, "tud_descriptor_device_cb", "Pointer to the device descriptor. VID 0xCAFE PID 0x4000."),
    (0x100008CC, "tud_descriptor_configuration_cb", "One MSC BOT interface, EP1 IN/OUT, 64-byte packets."),
    (0x100008D4, "tud_descriptor_string_cb", "Strings 1..4: PositiveLabs, RP2040 Flash MSC, 123456, Flash Disk."),
    (0x10000944, "encoder_irq", "GPIO27/29 quadrature, GPIO28 falling edge is the button."),
    (0x100009A4, "led_chase", "After a correct PIN: one digit-LED every 150 ms."),
    (0x10000AB0, "lock_ui", "Encoder plus 4 digits. Compared with bytes 06 00 06 01. USB starts only after return."),
    (0x10001100, "ws2812_init", "PIO on GPIO16, the RP2040-Zero onboard WS2812."),
    (0x10001218, "ws2812_put", "Pushes GRB<<8 into the PIO FIFO. Blue while entering, green on success."),
    (0x10001568, "gpio_set_pulls", "Writes pull-up/down in PADS_BANK0. Pins 27/28/29 are pulled up."),
    (0x10001590, "gpio_set_irq_enabled", "Event mask: 4=falling, 8=rising, 0xC=both."),
    (0x100015E8, "gpio_set_irq_enabled_with_callback", "Installs encoder_irq on GPIO29, both edges."),
    (0x100016B8, "gpio_init", "SIO function, clear OUT and OE, configure the pad."),
    (0x10001706, "panic", "Prints '*** PANIC ***' and halts. Pico SDK."),
    (0x1000187C, "panic_no_spinlocks", "String 'No spinlocks are available'."),
    (0x1000239C, "sleep_ms", "Timer sleep. 50 ms between PIN digits, 200 ms on failure."),
    (0x100025C8, "time_us_64", "Reads TIMER at 0x40054000. Lock and chase deadlines."),
    (0x10002E1C, "memcpy", "Used by inquiry, read10 and write10."),
    (0x10002E6C, "exit", "After main. Then bkpt."),
    (0x10002E74, "runtime_init", "Clocks, IRQs, allocators. First blx from reset_handler."),
    (0x1000305C, "empty_return_0", "Second call from main. Does nothing."),
    (0x100032C6, "pio_claim_unused_or_panic", "String 'No PIO state machines are available'."),
    (0x10003440, "usb_hw_init", "USBCTRL 0x50110000 / DPRAM 0x50100000."),
    (0x10003858, "tud_task", "TinyUSB main loop. main calls it with timeout -1."),
    (0x10004686, "msc_bot_task", "Bulk-Only transport. CBW signature 0x43425355 ('USBC')."),
    (0x10004E64, "tusb_init", "Brings up the stack. main calls this only after lock_ui returns."),
    (0x100050E0, "gpio25_output_init", "Pico board LED on GPIO25. Not the LED on an RP2040-Zero."),
    (0x100051C8, "strlen", "Word scan with 0xFEFEFEFF / 0x80808080."),
    (0x10005278, "flash_range_program", "Trampoline to SRAM 0x20000351. Cannot execute from XIP while programming."),
    (0x10005298, "flash_range_erase", "Trampoline to SRAM 0x200002C1. 4096-byte sector."),
    (0x100052C8, "flash_helper_sram", "Another SDK trampoline into the start of .data (0x200000C1)."),
]


LABELS = [
    (0x1000533C, "scsi_vendor_POSILABS", "8-byte Inquiry vendor."),
    (0x10005348, "scsi_product_FLASH_MSC", "16-byte Inquiry product, space padded."),
    (0x10005358, "usb_str_manufacturer", "PositiveLabs"),
    (0x10005368, "usb_str_product", "RP2040 Flash MSC"),
    (0x1000537C, "usb_str_serial", "123456"),
    (0x10005384, "usb_str_interface", "Flash Disk"),
    (0x10005390, "panic_banner", "*** PANIC ***"),
    (0x100053F8, "str_boot2_w25q080", None),
    (0x10005408, "str_version_0_1", None),
    (0x1000540C, "str_sdk_2_2_0", None),
    (0x10005414, "str_board_pico", None),
    (0x1000541C, "str_program_usb_token", None),
    (0x10005428, "str_build_date", "Mar 11 2026"),
    (0x100054BC, "usb_configuration_descriptor", "09 02 ... interface 08 06 50, EP1 bulk."),
    (0x100054DC, "usb_device_descriptor", "12 01, VID 0xCAFE, PID 0x4000, class EF/02/01."),
    (0x100054F0, "encoder_quad_table", "16 signed bytes: 0, +1, -1. Row = previous state, column = new state."),
    (0x10005500, "pin_code_6061", "Four digits lock_ui compares against: 6,0,6,1. Not ASCII."),
    (0x10005504, "progress_led_pins", "GPIO 13,12,11,10. How many digits are already confirmed."),
    (0x10005508, "digit_led_pins", "Digit 0..9 -> GPIO 7,6,5,4,3,2,1,0,9,8."),
    (0x10100000, "disk_image", "1 MiB FAT12 under XOR. LBA 0 is this address. Plaintext starts EB 3C 90."),
]




def run():
    # Image base can stay 0. What matters is that the flash block
    # already lives at 0x10000000 (the listing addresses start with 10000...).
    # Do NOT use Memory Map -> Set Image Base: that shifts every address.
    base = currentProgram.getImageBase()
    log("image base %s" % base)
    if not mem_has(A(0x10000000)) or not mem_has(A(0x100001F6)):
        log("STOP: no bytes at 0x10000000.")
        log("Window -> Memory Map -> select the firmware block -> Move -> start 10000000.")
        log("Do not use Set Image Base. That adds 0x10000000 to addresses that are already correct.")
        return
    log("flash block is at 0x10000000, continuing")
    fix_header()
    log("== functions ==")
    for off, name, comment in FUNCS:
        try:
            ensure_func(off, name, comment)
        except Exception, e:
            log("  FAIL %s: %s" % (name, e))
    log("== labels ==")
    for off, name, comment in LABELS:
        try:
            try_label(off, name, comment)
        except Exception, e:
            log("  FAIL %s: %s" % (name, e))
    try:
        currentProgram.getSymbolTable().addExternalEntryPoint(A(0x100001F6))
    except Exception, e:
        log("entry point: %s" % e)
    log("Done. Open main / lock_ui / tud_msc_read10_cb. Do not open boot2_w25q080.")




run()


