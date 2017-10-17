; ModuleID = 'test6.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: nounwind uwtable
define i32 @f(i32 %x) #0 {
entry:
  %x.addr = alloca i32, align 4
  store i32 %x, i32* %x.addr, align 4
  %0 = load i32* %x.addr, align 4
  %mul = mul nsw i32 %0, 2
  store i32 %mul, i32* %x.addr, align 4
  %1 = load i32* %x.addr, align 4
  ret i32 %1
}

; Function Attrs: nounwind uwtable
define i32 @main(i32 %argc, i8** %argv) #0 {
entry:
  %retval = alloca i32, align 4
  %argc.addr = alloca i32, align 4
  %argv.addr = alloca i8**, align 8
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  %c = alloca i32, align 4
  store i32 0, i32* %retval
  store i32 %argc, i32* %argc.addr, align 4
  store i8** %argv, i8*** %argv.addr, align 8
  %0 = load i8*** %argv.addr, align 8
  %arrayidx = getelementptr inbounds i8** %0, i64 1
  %1 = load i8** %arrayidx, align 8
  %call = call i32 @atoi(i8* %1) #2
  store i32 %call, i32* %a, align 4
  store i32 2048, i32* %b, align 4
  store i32 1664, i32* %c, align 4
  %2 = load i32* %a, align 4
  %cmp = icmp eq i32 %2, 1
  br i1 %cmp, label %if.then, label %if.else

if.then:                                          ; preds = %entry
  %3 = load i32* %b, align 4
  %call1 = call i32 @f(i32 %3)
  store i32 %call1, i32* %c, align 4
  br label %if.end

if.else:                                          ; preds = %entry
  %4 = load i32* %c, align 4
  %call2 = call i32 @f(i32 %4)
  store i32 %call2, i32* %b, align 4
  br label %if.end

if.end:                                           ; preds = %if.else, %if.then
  %5 = load i32* %b, align 4
  ret i32 %5
}

; Function Attrs: nounwind readonly
declare i32 @atoi(i8*) #1

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readonly "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind readonly }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"clang version 3.4.2 (tags/RELEASE_34/dot2-final)"}
