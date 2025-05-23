"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.iOS9Curve = void 0;
var iOS9Curve = /** @class */ (function () {
    function iOS9Curve(ctrl, definition) {
        this.GRAPH_X = 25;
        this.AMPLITUDE_FACTOR = 0.8;
        this.SPEED_FACTOR = 1;
        this.DEAD_PX = 2;
        this.ATT_FACTOR = 4;
        this.DESPAWN_FACTOR = 0.02;
        this.DEFAULT_NOOFCURVES_RANGES = [2, 5];
        this.DEFAULT_AMPLITUDE_RANGES = [0.3, 1];
        this.DEFAULT_OFFSET_RANGES = [-3, 3];
        this.DEFAULT_WIDTH_RANGES = [1, 3];
        this.DEFAULT_SPEED_RANGES = [0.5, 1];
        this.DEFAULT_DESPAWN_TIMEOUT_RANGES = [500, 2000];
        this.ctrl = ctrl;
        this.definition = definition;
        this.noOfCurves = 0;
        this.spawnAt = 0;
        this.prevMaxY = 0;
        this.phases = [];
        this.offsets = [];
        this.speeds = [];
        this.finalAmplitudes = [];
        this.widths = [];
        this.amplitudes = [];
        this.despawnTimeouts = [];
        this.verses = [];
    }
    iOS9Curve.prototype.getRandomRange = function (e) {
        return e[0] + Math.random() * (e[1] - e[0]);
    };
    iOS9Curve.prototype.spawnSingle = function (ci) {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        this.phases[ci] = 0;
        this.amplitudes[ci] = 0;
        this.despawnTimeouts[ci] = this.getRandomRange((_b = (_a = this.ctrl.opt.ranges) === null || _a === void 0 ? void 0 : _a.despawnTimeout) !== null && _b !== void 0 ? _b : this.DEFAULT_DESPAWN_TIMEOUT_RANGES);
        this.offsets[ci] = this.getRandomRange((_d = (_c = this.ctrl.opt.ranges) === null || _c === void 0 ? void 0 : _c.offset) !== null && _d !== void 0 ? _d : this.DEFAULT_OFFSET_RANGES);
        this.speeds[ci] = this.getRandomRange((_f = (_e = this.ctrl.opt.ranges) === null || _e === void 0 ? void 0 : _e.speed) !== null && _f !== void 0 ? _f : this.DEFAULT_SPEED_RANGES);
        this.finalAmplitudes[ci] = this.getRandomRange((_h = (_g = this.ctrl.opt.ranges) === null || _g === void 0 ? void 0 : _g.amplitude) !== null && _h !== void 0 ? _h : this.DEFAULT_AMPLITUDE_RANGES);
        this.widths[ci] = this.getRandomRange((_k = (_j = this.ctrl.opt.ranges) === null || _j === void 0 ? void 0 : _j.width) !== null && _k !== void 0 ? _k : this.DEFAULT_WIDTH_RANGES);
        this.verses[ci] = this.getRandomRange([-1, 1]);
    };
    iOS9Curve.prototype.getEmptyArray = function (count) {
        return new Array(count);
    };
    iOS9Curve.prototype.spawn = function () {
        var _a, _b;
        this.spawnAt = Date.now();
        this.noOfCurves = Math.floor(this.getRandomRange((_b = (_a = this.ctrl.opt.ranges) === null || _a === void 0 ? void 0 : _a.noOfCurves) !== null && _b !== void 0 ? _b : this.DEFAULT_NOOFCURVES_RANGES));
        this.phases = this.getEmptyArray(this.noOfCurves);
        this.offsets = this.getEmptyArray(this.noOfCurves);
        this.speeds = this.getEmptyArray(this.noOfCurves);
        this.finalAmplitudes = this.getEmptyArray(this.noOfCurves);
        this.widths = this.getEmptyArray(this.noOfCurves);
        this.amplitudes = this.getEmptyArray(this.noOfCurves);
        this.despawnTimeouts = this.getEmptyArray(this.noOfCurves);
        this.verses = this.getEmptyArray(this.noOfCurves);
        for (var ci = 0; ci < this.noOfCurves; ci++) {
            this.spawnSingle(ci);
        }
    };
    iOS9Curve.prototype.globalAttFn = function (x) {
        return Math.pow(this.ATT_FACTOR / (this.ATT_FACTOR + Math.pow(x, 2)), this.ATT_FACTOR);
    };
    iOS9Curve.prototype.sin = function (x, phase) {
        return Math.sin(x - phase);
    };
    iOS9Curve.prototype.yRelativePos = function (i) {
        var y = 0;
        for (var ci = 0; ci < this.noOfCurves; ci++) {
            // Generate a static T so that each curve is distant from each oterh
            var t = 4 * (-1 + (ci / (this.noOfCurves - 1)) * 2);
            // but add a dynamic offset
            t += this.offsets[ci];
            var k = 1 / this.widths[ci];
            var x = i * k - t;
            y += Math.abs(this.amplitudes[ci] * this.sin(this.verses[ci] * x, this.phases[ci]) * this.globalAttFn(x));
        }
        // Divide for NoOfCurves so that y <= 1
        return y / this.noOfCurves;
    };
    iOS9Curve.prototype.yPos = function (i) {
        return (this.AMPLITUDE_FACTOR *
            this.ctrl.heightMax *
            this.ctrl.amplitude *
            this.yRelativePos(i) *
            this.globalAttFn((i / this.GRAPH_X) * 2));
    };
    iOS9Curve.prototype.xPos = function (i) {
        return this.ctrl.width * ((i + this.GRAPH_X) / (this.GRAPH_X * 2));
    };
    iOS9Curve.prototype.drawSupportLine = function () {
        var ctx = this.ctrl.ctx;
        var coo = [0, this.ctrl.heightMax, this.ctrl.width, 1];
        var gradient = ctx.createLinearGradient.apply(ctx, coo);
        gradient.addColorStop(0, "transparent");
        gradient.addColorStop(0.1, "rgba(255,255,255,.5)");
        gradient.addColorStop(1 - 0.1 - 0.1, "rgba(255,255,255,.5)");
        gradient.addColorStop(1, "transparent");
        ctx.fillStyle = gradient;
        ctx.fillRect.apply(ctx, coo);
    };
    iOS9Curve.prototype.draw = function () {
        var ctx = this.ctrl.ctx;
        ctx.globalAlpha = 0.7;
        ctx.globalCompositeOperation = this.ctrl.opt.globalCompositeOperation;
        if (this.spawnAt === 0) {
            this.spawn();
        }
        if (this.definition.supportLine) {
            // Draw the support line
            return this.drawSupportLine();
        }
        for (var ci = 0; ci < this.noOfCurves; ci++) {
            if (this.spawnAt + this.despawnTimeouts[ci] <= Date.now()) {
                this.amplitudes[ci] -= this.DESPAWN_FACTOR;
            }
            else {
                this.amplitudes[ci] += this.DESPAWN_FACTOR;
            }
            this.amplitudes[ci] = Math.min(Math.max(this.amplitudes[ci], 0), this.finalAmplitudes[ci]);
            this.phases[ci] = (this.phases[ci] + this.ctrl.speed * this.speeds[ci] * this.SPEED_FACTOR) % (2 * Math.PI);
        }
        var maxY = -Infinity;
        var minX = +Infinity;
        // Write two opposite waves
        for (var _i = 0, _a = [1, -1]; _i < _a.length; _i++) {
            var sign = _a[_i];
            ctx.beginPath();
            for (var i = -this.GRAPH_X; i <= this.GRAPH_X; i += this.ctrl.opt.pixelDepth) {
                var x = this.xPos(i);
                var y = this.yPos(i);
                ctx.lineTo(x, this.ctrl.heightMax - sign * y);
                minX = Math.min(minX, x);
                maxY = Math.max(maxY, y);
            }
            ctx.closePath();
            ctx.fillStyle = "rgba(".concat(this.definition.color, ", 1)");
            ctx.strokeStyle = "rgba(".concat(this.definition.color, ", 1)");
            ctx.fill();
        }
        if (maxY < this.DEAD_PX && this.prevMaxY > maxY) {
            this.spawnAt = 0;
        }
        this.prevMaxY = maxY;
        return null;
    };
    iOS9Curve.getDefinition = function () {
        return [
            {
                color: "255,255,255",
                supportLine: true,
            },
            {
                // blue
                color: "15, 82, 169",
            },
            {
                // red
                color: "173, 57, 76",
            },
            {
                // green
                color: "48, 220, 155",
            },
        ];
    };
    return iOS9Curve;
}());
exports.iOS9Curve = iOS9Curve;
