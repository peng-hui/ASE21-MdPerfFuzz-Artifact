#!/usr/bin/env python3
import os

with open('MParserBaseVisitor.h', 'r') as input_f:
    code = input_f.read()
    code = code.replace('#include "antlr4-runtime.h"\n#include "MParserVisitor.h"', '#include <iostream>\n#include <vector>\n#include "antlr4-runtime.h"\n#include "MParserVisitor.h"\nusing namespace std;\nusing namespace antlr4;\n')
    code = code.replace('public:\n', 'public:\n\tvector<misc::Interval> intervals;\n\tvector<string> texts;\n\n')
with open('MParserBaseVisitor.h', 'w') as output_f:
    code1 = code.replace('override {\n', 'override {\n    intervals.push_back(ctx->getSourceInterval());\n    texts.push_back(ctx->start->getInputStream()->getText(ctx->getSourceInterval()));\n')
    output_f.write(code1)
with open('MParserSecondVisitor.h', 'w') as output_f:
    code2 = code.replace('override {\n', 'override {\n    //intervals.push_back(ctx->getSourceInterval());\n    texts.push_back(ctx->start->getInputStream()->getText(ctx->getSourceInterval()));\n')
    code2 = code2.replace('BaseVisitor', 'SecondVisitor')
    output_f.write(code2)

with open('MParserBaseVisitor.cpp', 'r') as input_f:
    code = input_f.read()
    code = code.replace('BaseVisitor', 'SecondVisitor')
with open('MParserSecondVisitor.cpp', 'w') as output_f:
    output_f.write(code)
