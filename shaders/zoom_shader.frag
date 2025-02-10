#version 330 core

uniform sampler2D tex;
uniform float time;
uniform vec2 resolution;
uniform vec3 gravity;
uniform vec3 speed;
uniform float zoom;

vec2 shadowShift = vec2(-0.005, 0.012);

in vec2 uvs;
out vec4 f_color;

float rand(vec2 n) { 
    return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
}

float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec2 uv = uvs;

    float shake = (noise(vec2(time)) - 0.5) * 0.0009;
    uv.x += shake;
    uv.y += (noise(vec2(time * 0.5)) - 0.5) * 0.0009;

    vec2 offset = vec2(0.001, 0.001);
    vec4 color = texture(tex, uv);

    float intensity = (sin(time * 2.0) * 0.5 + 0.5) * exp(-time * 0.1);

    color.r = texture(tex, uv + offset * vec2(-1.0, 0.5) * (1.0 + sin(time)) * 1.1).r + (gravity[0] * intensity * 0.05) + (speed[0] * intensity * 0.05);
    color.g = texture(tex, uv + offset * vec2(0.0, -0.5) * (1.0 + cos(time * 0.8)) * 1.2).g + (gravity[1] * intensity * 0.05) + (speed[1] * intensity * 0.05);
    color.b = texture(tex, uv + offset * vec2(1.0, 0.5) * (1.0 + sin(time * 1.2)) * 1.3).b + (gravity[2] * intensity * 0.05) + (speed[2] * intensity * 0.05);

    float scanline = sin(uv.y * 1000.0 + time * 10.0) * 0.1;
    color.rgb += scanline;

    color.rgb *= 0.9 + 0.1 * rand(uv + time);

    vec2 vig = uv - 0.5;
    color.rgb *= 1.0 - dot(vig, vig) * 1.5;

    color.rgb += (noise(uv * 50.0 + time) - 0.5) * 0.1 *zoom;

    color.rgb = mix(vec3(dot(color.rgb, vec3(0.299, 0.587, 0.114))), color.rgb, 0.1);
    color.rgb = mix(vec3(dot(color.rgb, vec3(0, 0, 0))), color.rgb, 0.9);

    f_color = color;
}
