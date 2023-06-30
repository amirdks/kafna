def form_error(form):
    error = 'مشکلی وجود دارد'
    field = "ارور"
    if form.errors:
        for field in form:
            for error in field.errors:
                error = error
                field = field.label
    if form.non_field_errors():
        for error in form.non_field_errors():
            error = error
    return f"{field} : {error}"
