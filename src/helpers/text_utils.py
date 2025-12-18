"""
Text processing utilities
"""
import re
import json
from typing import Any, Dict, List


def clean_html(text: str) -> str:
    """
    Remove HTML tags and clean up text formatting.
    
    Args:
        text: HTML text string
        
    Returns:
        Cleaned plain text string
        
    Examples:
        >>> clean_html("Hello<br/>World")
        "Hello\nWorld"
        
        >>> clean_html("<b>Bold</b> text")
        "Bold text"
    """
    if not text:
        return ""
    
    # Convert <br/> and <br> to newlines
    text = re.sub(r'<br\s*/?>', '\n', text)
    
    # Remove all other HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up extra whitespace and newlines
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()


def indent_text(text: str, indent: str = "   ") -> str:
    """
    Add indentation to each line of text.
    
    Args:
        text: Text to indent
        indent: Indentation string (default: 3 spaces)
        
    Returns:
        Indented text
    """
    lines = text.split('\n')
    return '\n'.join(indent + line if line.strip() else "" for line in lines)


def format_single_product(product: Dict[str, Any], index: int = 1) -> str:
    """
    Format a single product with ALL fields displayed.
    
    Args:
        product: Product dictionary from API
        index: Product number in the list
        
    Returns:
        Formatted product information string
    """
    lines = []
    
    # Header
    name = product.get('name', 'N/A')
    price = product.get('price', 0)
    price_str = f"{price:,}đ" if price > 0 else "Liên hệ"
    
    lines.append(f"【{index}】 {name}")
    lines.append(f"💰 Giá: {price_str}")
    lines.append("")
    
    # Basic Info
    lines.append("📋 THÔNG TIN CƠ BẢN:")
    lines.append(f"   • SKU: {product.get('sku', 'N/A')}")
    lines.append(f"   • ID: {product.get('id', 'N/A')}")
    lines.append(f"   • Slug: {product.get('slug', 'N/A')}")
    lines.append(f"   • Category ID: {product.get('categoryId', 'N/A')}")
    
    if product.get('origin'):
        lines.append(f"   • Xuất xứ: {product['origin']}")
    if product.get('brand'):
        lines.append(f"   • Thương hiệu: {product['brand']}")
    
    # Tags
    tags = product.get('tags', [])
    if tags:
        lines.append(f"   • Tags: {', '.join(tags)}")
    
    # Thumbnail
    thumbnail = product.get('thumbnailSmall', '')
    if thumbnail:
        lines.append(f"   • Hình ảnh: {thumbnail}")
    
    lines.append("")
    
    # Description
    description = product.get('description', '')
    if description:
        lines.append("📝 MÔ TẢ SẢN PHẨM:")
        clean_desc = clean_html(description)
        lines.append(indent_text(clean_desc, "   "))
        lines.append("")
    
    # Short Description
    short_desc = product.get('shortDescription', '')
    if short_desc:
        lines.append("📌 MÔ TẢ NGẮN:")
        clean_short = clean_html(short_desc)
        lines.append(indent_text(clean_short, "   "))
        lines.append("")
    
    # User Manual
    user_manual = product.get('userManual', '')
    if user_manual:
        lines.append("📖 HƯỚNG DẪN SỬ DỤNG:")
        clean_manual = clean_html(user_manual)
        lines.append(indent_text(clean_manual, "   "))
        lines.append("")
    
    # Storage Instructions
    storage = product.get('storageInstructions', '')
    if storage:
        lines.append("🏪 HƯỚNG DẪN BẢO QUẢN & CHẾ BIẾN:")
        clean_storage = clean_html(storage)
        lines.append(indent_text(clean_storage, "   "))
        lines.append("")
    
    return "\n".join(lines)


def format_api_product_response(data: Dict[str, Any]) -> str:
    """
    Format API product response data into a comprehensive readable format.
    Displays ALL product information including descriptions, manuals, and storage instructions.
    
    Args:
        data: API response data with structure {items: [], page, limit, total}
        
    Returns:
        Formatted string with complete product information
    """
    if not isinstance(data, dict) or 'items' not in data:
        return "Dữ liệu không hợp lệ"
    
    items = data.get('items', [])
    page = data.get('page', 1)
    limit = data.get('limit', 10)
    total = data.get('total', 0)
    
    output = []
    output.append("=" * 100)
    output.append(f"KẾT QUẢ TÌM KIẾM SẢN PHẨM")
    output.append(f"Trang {page} | Hiển thị {len(items)}/{total} sản phẩm")
    output.append("=" * 100)
    output.append("")
    
    for idx, item in enumerate(items, 1):
        product_info = format_single_product(item, idx)
        output.append(product_info)
        output.append("\n" + "-" * 100 + "\n")
    
    return "\n".join(output)


def print_api_response(data: Dict[str, Any]) -> None:
    """
    Print API product response in a formatted way.
    
    Args:
        data: API response data
    """
    formatted = format_api_product_response(data)
    print(formatted)


def parse_and_print_api_response(json_string: str) -> None:
    """
    Parse JSON string from API and print formatted product information.
    
    Args:
        json_string: JSON string from API response
        
    Examples:
        >>> json_data = '{"items": [...], "page": 1, "total": 3}'
        >>> parse_and_print_api_response(json_data)
    """
    try:
        data = json.loads(json_string)
        print_api_response(data)
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi parse JSON: {e}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")



